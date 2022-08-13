import re
import timeago
from datetime import datetime
from dateutil import parser

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class FootermatterPlugin(BasePlugin):
    config_scheme = (
        ('key_authors', config_options.Type(str, default='authors')),
        ('key_created', config_options.Type(str, default='created')),
        ('key_updated', config_options.Type(str, default='updated')),
        ("locale", config_options.Type(str, default='')),
        ('author_map', config_options.Type(list, default=[])),
        ("separator_map", config_options.Type(str, default='|')),
    )

    def __init__(self):
        self.author_map = {}

    def on_config(self, config: config_options.Config):
        # Set locale from theme / english, unless specified.
        if self.config['locale']:
            pass
        elif "language" in config.get("theme"):
            self.config['locale'] = config.get("theme")._vars.get("language")
        elif "locale" in config.get("theme"):
            self.config['locale'] = config.get("theme")._vars.get("locale")
        else:
            self.config['locale'] = 'en'

        for author in self.config.get('author_map'):
            key, img, url = author.split(self.config.get('separator_map'))
            self.author_map[key.strip()] = [key.strip(), img.strip(), url.strip()]

    def on_page_context(self, context, page, config, nav):
        a = page.meta.get(self.config.get("key_authors"))
        c = page.meta.get(self.config.get("key_created"))
        u = page.meta.get(self.config.get("key_updated"))
        if not a or not c or not u:
            return context
        a = a if isinstance(a, list) else [a]
        locale, now = self.config.get('locale'), datetime.now()
        context['footermatter_authors'] = [self.author_map.get(author) for author in a]
        context['footermatter_created'] = timeago.format(c, now, locale)
        context['footermatter_updated'] = timeago.format(u, now, locale)
        return context
