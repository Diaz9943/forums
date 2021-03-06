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
			'Alliance'	: self.format_evewho,
			'DebugTag' : self.format_logging
		}
		for tag, parser in self.standalone_available_tags.iteritems():
			self.parser.add_formatter(tag, parser, standalone = True)

	def format(self, text):
		return self.parser.format(text)

	def format_dotlan(self, tag_name, value, options, parent, context):
		return '<a href="http://evemaps.dotlan.net/%s/%s" target="dotlan">%s</a>' % ( tag_name.lower(), options[tag_name].replace(' ', '_'), options[tag_name] )

	def format_system(self, tag_name, value, options, parent, context):
		return '<a href="http://evemaps.dotlan.net/system/%s" target="dotlan">%s</a>' % ( options[tag_name], options[tag_name].replace(' ','_'), options[tag_name] )

	def format_evewho(self, tag_name, value, options, parent, context):
		path = {
			'corporation' : 'corp',
			'alliance' : 'ali',
			'character' : 'pilot'
		}[tag_name.lower()]
		return '<a href="http://evewho.com/%s/%s" target="evewho">%s</a>' % ( path, quote( options[tag_name] ), options[tag_name] )

	def format_logging(self, tag_name, value, options, parent, context):
		return "<pre>tag name=%s\nvalue=%s\noptions=%s\nparent=%s\ncontext=%s</pre>" % ( tag_name, value, options, parent, context )
