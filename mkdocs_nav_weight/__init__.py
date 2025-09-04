from numbers import Number
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs_nav_weight.nav_setter import NavSetter

# common strings
SECTION_RENAMED = "section_renamed"
INDEX_WEIGHT = "index_weight"
WARNING = "warning"
REVERSE = "reverse"
HEADLESS_INCLUDED = "headless_included"
DEFAULT_PAGE_WEIGHT = "default_page_weight"


class MkDocsNavWeight(BasePlugin):

    config_scheme = (
        (SECTION_RENAMED, config_options.Type(bool, default=False)),
        (INDEX_WEIGHT, config_options.Type(Number, default=-10)),
        (WARNING, config_options.Type(bool, default=True)),
        (REVERSE, config_options.Type(bool, default=False)),
        (HEADLESS_INCLUDED, config_options.Type(bool, default=False)),
        (DEFAULT_PAGE_WEIGHT, config_options.Type(Number, default=0)),
    )

    def on_nav(self, nav, config, files, **kwargs):
        setter = NavSetter(nav, self.config, config)
        return setter.set_nav()
