from numbers import Number
from warnings import catch_warnings
import mkdocs


class MkDocsNavWeight(mkdocs.plugins.BasePlugin):

    config_scheme = (
    )

    # add markdown and meta to page
    def _set_meta(self, element, config):
        for item in element:
            if item.is_section:
                self._set_meta(item.children, config)
            elif item.is_page:
                item.read_source(config)

    def _get_page_weight(self, page):
        try:
            # exist 'weight'
            # seems "isinstance" has an exception handling
            if isinstance(page.meta['weight'], Number):
                return page.meta['weight']
            else:
                print(f"[mkdocs-nav-weight]Warning: Invaild value for 'weight' in {page}, setting to 0")
                return 0
        except:
            # no `weight`
            print(f"[mkdocs-nav-weight]Warning: No 'weight' in {page}, setting to 0")
            return 0

    def _get_weight(self, element):
        # is a page and not index
        if element.is_page and not element.is_index:
            return self._get_page_weight(element)
        # is a section
        if element.is_section:
            # try to find "index.md" and get weight
            for child in element.children:
                if child.is_page and child.is_index:
                    return self._get_page_weight(child)
        # a link or index or no index section
        return 0

    def _sort_by_weight(self, element):
        element.children.sort(key=self._get_weight, reverse=False)
        for item in element.children:
            if item.is_section:
                self._sort_by_weight(item)

    def on_nav(self, nav, config, files, **kwargs):

        # set meta
        self._set_meta(nav, config)
        # sort nav
        nav.items.sort(key=self._get_weight, reverse=False)
        for item in nav.items:
            if item.is_section:
                self._sort_by_weight(item)

        return nav
