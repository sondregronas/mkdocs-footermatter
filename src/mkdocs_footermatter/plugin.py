import pendulum

from dateutil import parser
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

# TODO: Add more aliases
LOCALE_ALIASES = {
    'nb_NO': 'nb',
    'nb_NN': 'nn',
    'no': 'nb',
    'en_US': 'en'
}


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
        ("date_format", config_options.Type(str, default='date')),
        ('author_map', config_options.Type(list, default=[])),
        ("separator_map", config_options.Type(str, default='|')),
        ("default_author_img", config_options.Type(str, default='https://ui-avatars.com')),
        ("default_author_url", config_options.Type(str, default='/')),
    )

    def __init__(self):
        self.author_map = {}
        self.now = pendulum.now()

    def on_config(self, config: config_options.Config):
        """Define locale (from theme or specified) and authors from mkdocs.yml"""
        self.config['locale'] = str(self.get_locale(config))
        if self.config['locale'] in LOCALE_ALIASES.keys():  # pragma: no cover
            self.config['locale'] = LOCALE_ALIASES.get(self.config['locale'])

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
    def get_locale(self, config: config_options.Config, fallback='en'):
        """Returns the locale in the given priority (specified, theme language, theme locale, en)"""
        if self.config.get('locale'):
            return self.config.get('locale')
        elif "theme" in config and "locale" in config.get("theme"):
            return config.get("theme")._vars.get("locale", fallback)
        elif "theme" in config and "language" in config.get("theme"):
            return config.get("theme")._vars.get("language", fallback)
        return fallback

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

    def format_timeago(self, diff) -> str:
        if diff.years:
            return self.now.subtract(years=diff.years).diff_for_humans()
        if diff.months:
            return self.now.subtract(months=diff.months).diff_for_humans()
        if diff.weeks:
            return self.now.subtract(weeks=diff.weeks).diff_for_humans()
        if diff.days:
            return self.now.subtract(days=diff.days).diff_for_humans()
        if diff.hours:
            return self.now.subtract(hours=diff.hours).diff_for_humans()
        if diff.minutes:
            return self.now.subtract(minutes=diff.minutes).diff_for_humans()
        return self.now.subtract(seconds=diff.seconds).diff_for_humans()


    def format_date(self, date):
        """Takes a date value and formats it to the given format"""
        if date is None:  # pragma: no cover
            return

        df, locale = self.config.get('date_format'), self.config.get('locale')
        date = parser.parse(date) if isinstance(date, str) else date
        date = pendulum.instance(date)

        try:
            pendulum.set_locale(locale)
        except ValueError:  # pragma: no cover
            print(f'[WARNING]: Locale for mkdocs-footermatter is invalid (Got: {locale})')
            print(f'[WARNING]: Locale for mkdocs-footermatter is now set to \'en\'.')
            pendulum.set_locale('en')

        options = {
            'timeago': self.format_timeago(self.now - date),
            'date': date.format(fmt="LL"),
            'datetime': date.format(fmt='LLL')
        }

        return options.get(df, date.format(fmt=df))
