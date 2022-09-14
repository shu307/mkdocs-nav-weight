from numbers import Number
from warnings import catch_warnings
import mkdocs


class MkDocsNavWeight(mkdocs.plugins.BasePlugin):

    config_scheme = (
        ('section_renamed', mkdocs.config.config_options.Type(bool, default=False)),
        ('reverse', mkdocs.config.config_options.Type(bool, default=False)),
    )

    _is_section_renamed = False
    _is_reverse = False

    # add markdown and meta to page
    def _set_meta(self, element, config):
        for item in element:
            if item.is_section:
                self._set_meta(item.children, config)
            elif item.is_page:
                item.read_source(config)

    def _get_title_from_index(self, section, index):
        try:
            section.title = index.title
        except:
            return

    def _get_page_weight(self, page):
        try:
            # exist "weight"
            if isinstance(page.meta['weight'], Number):
                return page.meta['weight']
            else:
                print(
                    f"[mkdocs-nav-weight]Warning: Invaild value for 'weight' in {page}, setting to 0")
                return 0
        except:
            # no "weight"
            print(
                f"[mkdocs-nav-weight]Warning: No 'weight' in {page}, setting to 0")
            return 0

    def _get_weight(self, element):
        # is a page and not index
        if element.is_page and not element.is_index:
            return self._get_page_weight(element)
        # is a section
        if element.is_section:
            # try to find "index.md"
            for child in element.children:
                # exist "index.md"
                if child.is_page and child.is_index:
                    if self._is_section_renamed:
                        # get title form index
                        self._get_title_from_index(element, child)
                    # return weight from index
                    return self._get_page_weight(child)
        # a link or index or no index section
        return 0

    def _sort_by_weight(self, element):
        element.children.sort(key=self._get_weight, reverse=self._is_reverse)
        for item in element.children:
            if item.is_section:
                self._sort_by_weight(item)

    # get option
    def on_pre_build(self, config, **kwargs):
        self._is_section_renamed = self.config["section_renamed"]
        self._is_reverse = self.config["reverse"]

    # set nav
    def on_nav(self, nav, config, files, **kwargs):
        # set meta
        self._set_meta(nav, config)
        # sort nav
        nav.items.sort(key=self._get_weight, reverse=self._is_reverse)
        for item in nav.items:
            if item.is_section:
                self._sort_by_weight(item)

        return nav
