from numbers import Number
import mkdocs
from mkdocs_nav_weight.util import Util


class MkDocsNavWeight(mkdocs.plugins.BasePlugin):

    config_scheme = (
        ('section_renamed', mkdocs.config.config_options.Type(bool, default=False)),
        ('index_weight', mkdocs.config.config_options.Type(Number, default=-10)),
        ('warning', mkdocs.config.config_options.Type(bool, default=True)),
        ('reverse', mkdocs.config.config_options.Type(bool, default=False)),
    )

    def on_nav(self, nav, config, files, **kwargs):
        util = Util(self.config, nav.items, nav.pages, config)
        util.set_nav()
        return nav
