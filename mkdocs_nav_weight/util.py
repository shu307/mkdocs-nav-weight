import logging
from numbers import Number

log = logging.getLogger("mkdocs.plugins")


class Util():
    def __init__(self, plugin_config, nav_items, nav_pages, config) -> None:
        self._is_section_renamed = plugin_config["section_renamed"]
        self._is_reverse = plugin_config["reverse"]
        self._is_warning = plugin_config["warning"]
        self._index_weight = plugin_config["index_weight"]
        self._headless_included = plugin_config["headless_included"]

        self._nav_items = nav_items
        self._nav_pages = nav_pages
        self._config = config

        self._section_weights = {}

        self._empty_items = []
        self._headless_items = []

    def _get_meta(self, key, default, type, page):
        meta = page.meta
        if key in meta.keys():
            if isinstance(meta[key], type):
                return meta[key]
            else:
                # option: "warning"
                if self._is_warning:
                    log.warning(
                        f"[mkdocs-nav-weight]: Invaild value for \"{key}\" in {page}, setting to \"{default}\"")
        return default

    def _get_weight(self, item):
        if item.is_page:
            if item.is_index:
                return self._index_weight
            return self._get_meta("weight", 0, Number, item)
        if item.is_section:
            if item in self._section_weights.keys():
                return self._section_weights[item]
        # no_index section or link
        return 0

    def _sort_items(self, items):
        for item in items:
            if item.is_page:
                item.read_source(self._config)
                # index
                if item.is_index:
                    # do nothing if it's a top level "index"
                    if item.parent:
                        self._section_weights[item.parent] = self._get_meta(
                            "weight", 0, Number, item)
                        # option: "section_renamed"
                        if self._is_section_renamed:
                            item.parent.title = item.title
                        elif self._get_meta("retitled", False, bool, item):
                            item.parent.title = item.title

                        if self._get_meta("empty", False, bool, item):
                            self._empty_items.append(item)

                        if self._get_meta("headless", False, bool, item):
                            self._headless_items.append(item.parent)
                # normal page
                elif self._get_meta("headless", False, bool, item):
                    self._headless_items.append(item)

            elif item.is_section:
                self._sort_items(item.children)

        items.sort(key=self._get_weight, reverse=self._is_reverse)

    def _connect_items_rec(self, items, temp_page):
        for item in items:
            if item.is_page:
                item.previous_page = temp_page
                if temp_page:
                    temp_page.next_page = item
                temp_page = item
                # continue
            elif item.is_section:
                self._connect_items_rec(item.children, temp_page)

    def _connect_items(self, items):
        temp_page = None
        self._connect_items_rec(items, temp_page)
        if temp_page:
            temp_page.next_page = None

    def _isolate_item(self, item):
        # page
        if item.is_page:
            if item.previous_page:
                item.previous_page.next_page = item.next_page
            if item.next_page:
                item.next_page.previous_page = item.previous_page
            item.previous_page = None
            item.next_page = None
        # section
        elif item.is_section:
            self._connect_items(item.children)

        # is top level?
        if item.parent:
            item.parent.children.remove(item)
        else:
            self._nav_items.remove(item)

    def _set_items(self):

        for item in self._empty_items:
            self._isolate_item(item)

        # isolate headless items
        for item in self._headless_items:
            self._isolate_item(item)

        # connect normal items
        self._connect_items(self._nav_items)

    def _get_pages(self, items):
        pages = []

        for item in items:
            if item.is_page:
                pages.append(item)

            elif item.is_section:
                pages.extend(self._get_pages(item.children))

        return pages

    def set_nav(self):
        # nav_items
        self._sort_items(self._nav_items)
        self._set_items()

        # nav_pages
        self._nav_pages = self._get_pages(self._nav_items)
        if self._headless_included:
            self._nav_pages.extend(self._get_pages(self._headless_items))
