from numbers import Number

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from mkdocs_nav_weight.util import Util


class MkDocsNavWeight(BasePlugin):

    config_scheme = (
        ('section_renamed', config_options.Type(bool, default=False)),
        ('index_weight', config_options.Type(Number, default=-10)),
        ('warning', config_options.Type(bool, default=True)),
        ('reverse', config_options.Type(bool, default=False)),
        ('headless_included', config_options.Type(bool, default=False)),
    )

    def on_nav(self, nav, config, files, **kwargs):
        util = Util(self.config, nav.items, nav.pages, config)
        util.set_nav()
        return nav
