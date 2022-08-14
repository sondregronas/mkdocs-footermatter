import pytest
import datetime

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
    cfg = {'theme': Vars({'language': 'test1'})}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'test1'

    # Ensure locale from theme works
    cfg = {'theme': Vars({'locale': 'test2'})}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'test2'

    # Ensure fallback locale works
    cfg = {'': ''}
    plugin.config['locale'] = None
    assert plugin.get_locale(cfg) == 'en'


def test_plugin(plugin):
    page = Page({'authors': 'Test Author', 'created': datetime.date(2022, 1, 1), 'updated': datetime.date(2022, 1, 1)})
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

    page = Page({'created': datetime.date(2022, 1, 1), 'updated': datetime.date(2022, 1, 1)})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is None
    assert context_after.get('footermatter_created') is not None
    assert context_after.get('footermatter_updated') is not None

    page = Page({'authors': 'Test Author'})
    context_after = plugin.on_page_context({}, page)
    assert context_after.get('footermatter_authors') is not None
    assert context_after.get('footermatter_created') is None
    assert context_after.get('footermatter_updated') is None
