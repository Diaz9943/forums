# encoding: utf-8

from __future__ import unicode_literals
from bbcode import Parser
from urllib import quote

log = __import__('logging').getLogger(__name__)

class SemanticTagParser(object):
    def __init__(self):
        self.parser = Parser()
        self.standalone_available_tags = {
            'System' : self.format_dotlan,
            'Region' : self.format_dotlan,
            'Character' : self.format_evewho,
            'Corporation' : self.format_evewho,
            'Alliance'  : self.format_evewho,
            'DebugTag' : self.format_logging
        }
        self.block_available_tags = {
            'Spoilers' : self.format_spoilers,
        }
        for tag, parser in self.standalone_available_tags.iteritems():
            self.parser.add_formatter(tag, parser, standalone = True)
        for tag, parser in self.block_available_tags.iteritems():
            self.parser.add_formatter(tag, parser, standalone = False)

    def format(self, text):
        return self.parser.format(text)

    def format_dotlan(self, tag_name, value, options, parent, context):
        return '<a href="http://evemaps.dotlan.net/%s/%s" target="dotlan">%s</a>' % ( tag_name.lower(), options[tag_name].replace(' ', '_'), options[tag_name] )

    def format_evewho(self, tag_name, value, options, parent, context):
        path = {
            'corporation' : 'corp',
            'alliance' : 'ali',
            'character' : 'pilot'
        }[tag_name.lower()]
        return '<a href="http://evewho.com/%s/%s" target="evewho">%s</a>' % ( path, quote( options[tag_name] ), options[tag_name] )

    def format_logging(self, tag_name, value, options, parent, context):
        return "<pre>tag name=%s\nvalue=%s\noptions=%s\nparent=%s\ncontext=%s</pre>" % ( tag_name, value, options, parent, context )

    def format_spoilers(self, tag_name, value, options, parent, context):
        if not tag_name in options:
            options[tag_name] = "Spoilers..."
        return ("<div class='spoiler-container'>"
                    "<a href='#' class='target fa fa-plus-square fa-fw fa-lg'></a>"
                    "<span class='description'>%s</span>"
                    "<div class='spoilers'>%s</div>"
                "</div>" %
                (options[tag_name], value))
