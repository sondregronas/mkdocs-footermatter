import timeago
from datetime import datetime

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class Author:
    def __init__(self, name, img, url):
        self.name = name
        self.img = img
        self.url = url


class FootermatterPlugin(BasePlugin):
    config_scheme = (
        ('key_authors', config_options.Type(str, default='authors')),
        ('key_created', config_options.Type(str, default='created')),
        ('key_updated', config_options.Type(str, default='updated')),
        ("locale", config_options.Type(str, default='')),
        ("date_format", config_options.Type(str, default='timeago')),
        ('author_map', config_options.Type(list, default=[])),
        ("separator_map", config_options.Type(str, default='|')),
        ("default_author_img",
         config_options.Type(str, default='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')),
        ("default_author_url", config_options.Type(str, default='/')),
    )

    def __init__(self):
        self.author_map = {}
        self.now = datetime.now()

    def on_config(self, config: config_options.Config):
        """Define locale (from theme or specified) and authors from mkdocs.yml"""
        self.config['locale'] = self.get_locale(config)
        self.author_map = {name.strip(): Author(name.strip(), img.strip(), url.strip())
                           for name, img, url in [author.split(self.config['separator_map'])
                                                  for author in self.config['author_map']]}

    def on_page_context(self, context, page, **kwargs):
        """Generate context values for the template, but only if all values exist"""
        authors, created, updated = self.get_frontmatter_keys(page)
        if authors and created and updated:
            context['footermatter_authors'] = [self.get_author(a) for a in authors]
            context['footermatter_created'] = self.format_date(created)
            context['footermatter_updated'] = self.format_date(updated)
        return context

    # Util functions
    def get_locale(self, config: config_options.Config) -> str:
        """Returns the locale in the given priority (specified, theme language, theme locale, en)"""
        return self.config.get('locale') \
               or config.get("theme")._vars.get("language") \
               or config.get("theme")._vars.get("locale") \
               or 'en'

    def get_author(self, author) -> Author:
        """Returns either a defined author from author_map, or creates a new one using default values"""
        return self.author_map.get(author,
                                   Author(author, self.config.get('default_author_img'),
                                          self.config.get('default_author_url')))

    def get_frontmatter_keys(self, page) -> tuple:
        """Returns a tuple for the fronmatter values of authors, created and updated"""
        authors = page.meta.get(self.config.get("key_authors"))
        if authors is not None:  # Ensure authors is list
            authors = authors if isinstance(authors, list) else [authors]
        created = page.meta.get(self.config.get("key_created"))
        updated = page.meta.get(self.config.get("key_updated"))
        return authors, created, updated

    def format_date(self, date):
        """Takes a date value and formats it to the given format"""
        df, locale = self.config.get('date_format'), self.config.get('locale')
        if df == 'timeago':
            return timeago.format(date, self.now, locale)
        raise NotImplementedError(f'Dateformat not implemented ({df})')
