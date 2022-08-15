import timeago
from datetime import datetime
from dateutil import parser
from babel.dates import format_date

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
        ("default_author_img", config_options.Type(str, default='https://ui-avatars.com')),
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
        context['footermatter_authors'] = [self.get_author(a) for a in authors] if authors else None
        context['footermatter_created'] = self.format_date(created) if created else None
        context['footermatter_updated'] = self.format_date(updated) if updated else None
        return context

    ###
    # Util functions
    ###
    def get_locale(self, config: config_options.Config) -> str:
        """Returns the locale in the given priority (specified, theme language, theme locale, en)"""
        if self.config.get('locale'):
            return self.config.get('locale')
        elif "theme" in config and "locale" in config.get("theme"):
            return config.get("theme")._vars.get("locale")
        elif "theme" in config and "language" in config.get("theme"):
            return config.get("theme")._vars.get("language")
        return 'en'

    def get_author(self, author) -> Author:
        """Returns either a defined author from author_map, or creates a new one using default values"""
        if author not in self.author_map:
            return Author(author, self.config.get('default_author_img'), self.config.get('default_author_url'))
        return self.author_map.get(author)

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
        if date is None:  # pragma: no cover
            return

        df, locale = self.config.get('date_format'), self.config.get('locale')
        date = parser.parse(date) if isinstance(date, str) else date

        options = {
            'timeago': timeago.format(date, self.now, locale),
            'date': format_date(date, format="long", locale=locale),
            'datetime': " ".join([format_date(date, format="long", locale=locale), date.strftime('%H:%M:%S')]),
        }

        return options.get(df, date.strftime(df))

