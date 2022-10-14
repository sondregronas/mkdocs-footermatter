import pytest
import pendulum
from pendulum import datetime

from mkdocs_footermatter.plugin import FootermatterPlugin
from mkdocs.config import config_options


class Vars:
    def __init__(self, dict):
        self._vars = dict

    def __getitem__(self, name):
        return self._vars[name]

    def __iter__(self):
        return iter(self._vars)

    def keys(self):
        return self._vars.keys()

    def items(self):
        return self._vars.items()

    def values(self):
        return self._vars.values()


class Page():
    def __init__(self, meta):
        self.meta = meta


@pytest.fixture
def plugin():
    plugin = FootermatterPlugin()
    plugin.load_config(options={})
    plugin.on_config(plugin.config)
    return plugin


def test_locale(plugin):
    # Ensure specified locale works
    cfg = config_options.BaseConfigOption().default
    plugin.config['locale'] = 'test'
    assert plugin.get_locale(cfg) == 'test'

    # Ensure language from theme works
    cfg = {'theme': Vars({'language': 'nb'})}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'nb'

    # Ensure locale from theme works
    cfg = {'theme': Vars({'locale': 'nn'})}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'nn'

    # Ensure fallback locale works
    cfg = {'': ''}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'en'


def test_plugin(plugin):
    page = Page({'authors': 'Test Author', 'created': datetime(2022, 1, 1), 'updated': datetime(2022, 1, 1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is not None
    assert context_after.get('footermatter_authors')[0].name == 'Test Author'
    assert context_after.get('footermatter_authors')[0].img is plugin.config['default_author_img']
    assert context_after.get('footermatter_authors')[0].url is plugin.config['default_author_url']
    assert context_after.get('footermatter_created') is not None
    assert context_after.get('footermatter_updated') is not None

    plugin.config['author_map'] = ['Test Author | test_image | test_url']
    plugin.on_config(plugin.config)
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors')[0].img == 'test_image'
    assert context_after.get('footermatter_authors')[0].url == 'test_url'

    page = Page({})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is None
    assert context_after.get('footermatter_created') is None
    assert context_after.get('footermatter_updated') is None

    page = Page({'created': datetime(2022, 1, 1), 'updated': datetime(2022, 1, 1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is None
    assert context_after.get('footermatter_created') is not None
    assert context_after.get('footermatter_updated') is not None

    page = Page({'authors': 'Test Author'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is not None
    assert context_after.get('footermatter_created') is None
    assert context_after.get('footermatter_updated') is None


def test_formats(plugin):
    # Date
    plugin.config['date_format'] = 'date'
    page = Page({'created': '2022-02-01 10:00'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'February 1, 2022'

    page = Page({'created': '01 feb.22'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'February 1, 2022'

    page = Page({'created': 'feb 1 2022'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'February 1, 2022'

    # Datetime
    plugin.config['date_format'] = 'datetime'
    plugin.config['locale'] = 'en'
    page = Page({'created': 'feb 1 2022'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'February 1, 2022 12:00 AM'

    plugin.config['locale'] = 'nb'
    page = Page({'created': '2022-02-01 12:00'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '1. februar 2022 12:00'

    plugin.config['locale'] = 'en'
    page = Page({'created': '2022-02-01 12:00'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'February 1, 2022 12:00 PM'

    # Custom
    plugin.config['locale'] = 'en'
    plugin.config['date_format'] = 'HH:mm:ss'
    page = Page({'created': '2022-02-01 12:00'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '12:00:00'

    plugin.config['date_format'] = 'YY-YYYY-MM-mm'
    page = Page({'created': '2022-02-01 12:30'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '22-2022-02-30'

    # Timeago
    plugin.config['date_format'] = 'timeago'
    page = Page({'created': pendulum.now().subtract(months=30, seconds=1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '2 years ago'

    page = Page({'created': pendulum.now().subtract(minutes=30, seconds=1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '30 minutes ago'

    page = Page({'created': pendulum.now().subtract(days=2, seconds=1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == '2 days ago'

    page = Page({'created': pendulum.now().subtract(seconds=5)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_created') == 'a few seconds ago'
