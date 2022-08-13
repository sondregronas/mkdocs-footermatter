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
        self.data = {}
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

    def on_page_markdown(self, markdown, page, config, files):
        if not markdown.startswith('---'):
            return markdown
        frontmatter = markdown.split('---')[1]

        self.data['authors'] = extract_authors(self.config.get("key_authors"), frontmatter)
        if not self.data.get('authors'):
            return markdown

        for line in frontmatter.split('\n'):
            created = re.match(self.config.get("key_created") + r': *(.+)', line)
            updated = re.match(self.config.get("key_updated") + r': *(.+)', line)
            if created:
                self.data['created'] = readable_date(created.group(1).strip(), self.config['locale'])
            elif updated:
                self.data['updated'] = readable_date(updated.group(1).strip(), self.config['locale'])

    def on_page_context(self, context, page, config, nav):
        if not self.data.get('authors') or not self.data.get('updated') or not self.data.get('created'):
            return context
        context['footermatter_authors'] = [self.author_map.get(author) for author in self.data.get('authors')]
        context['footermatter_created'] = self.data.get('created', '')
        context['footermatter_updated'] = self.data.get('updated', '')
        return context


def readable_date(date, locale) -> str:
    return timeago.format(parser.parse(date), datetime.now(), locale)


def extract_authors(key, frontmatter) -> list:
    out = list()
    is_list = False
    for line in frontmatter.split('\n'):
        # read authors: Firstname Lastname
        single_author = re.match(key + r': *(\w.+)', line)
        if single_author:
            return [single_author.group(1)]

        # read authors: [Firstname Lastname, Firstname2 Lastname2]
        authors_bracket = re.match(key + r': *\[(.+)\]', line)
        if authors_bracket:
            return [author.strip() for author in authors_bracket.group(1).split(',')]

        # read authors:
        #       - firstname lastname
        #       - firstname2 lastname2
        elif re.match(key + r': *$', line):
            is_list = True
        elif is_list and not line.strip().startswith('-'):
            is_list = False
        elif is_list:
            author = line.split('-')[1].strip()
            if author:
                out += [author]
    return out
