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
        # exist key 'weight'
        if page.meta and page.meta['weight']:
            return page.meta['weight']
        # no key
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

    def _sort_by_weight(self, element, is_nav):

        if is_nav:
            enumerable = element.items
        else:
            enumerable = element.children
        
        enumerable.sort(key=self._get_weight, reverse=False)
        for item in enumerable:
            if item.is_section:
                self._sort_by_weight(item, False)

    def on_nav(self, nav, config, files, **kwargs):

        # set meta
        self._set_meta(nav, config)
        # sort nav
        self._sort_by_weight(nav, True)
        # print(nav)
        return nav
