import logging
from numbers import Number

log = logging.getLogger("mkdocs.plugins")


class Util():
    def __init__(self, plugin_config, nav_items, config) -> None:
        self._is_section_renamed = plugin_config["section_renamed"]
        self._is_reverse = plugin_config["reverse"]
        self._is_warning = plugin_config["warning"]
        self._index_weight = plugin_config["index_weight"]

        self._nav_items = nav_items
        self._config = config

        self._section_weights = {}
        self._temp_page = None
        self._to_delete_items = []

    def _get_page_meta(self, key, default, type, page):
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
            return self._get_page_meta("weight", 0, Number, item)
        if item.is_section:
            if item in self._section_weights.keys():
                return self._section_weights[item]
        # no_index section or link
        return 0

    def _organize_nav(self, items):
        for item in items:
            if item.is_page:
                item.read_source(self._config)
                # index
                if item.is_index:
                    # do nothing if it's a top level "index"
                    if item.parent:
                        self._section_weights[item.parent] = self._get_page_meta(
                            "weight", 0, Number, item)
                        # option: "section_renamed"
                        if self._is_section_renamed:
                            item.parent.title = item.title
                        elif self._get_page_meta("retitled", False, bool, item):
                            item.parent.title = item.title

                        if self._get_page_meta("empty", False, bool, item):
                            self._to_delete_items.append(item)
                        if self._get_page_meta("headless", False, bool, item):
                            self._to_delete_items.append(item.parent)
                # normal page
                elif self._get_page_meta("headless", False, bool, item):
                    self._to_delete_items.append(item)

            elif item.is_section:
                self._organize_nav(item.children)

        items.sort(key=self._get_weight, reverse=self._is_reverse)

    def _connect_pages(self, items):
        for item in items:
            if item.is_page:
                item.previous_page = self._temp_page
                if self._temp_page:
                    self._temp_page.next_page = item
                self._temp_page = item
                # continue
            elif item.is_section:
                self._connect_pages(item.children)

    def _organize_pages(self):
        # "self._to_delete_items" contains no "link"
        for item in self._to_delete_items:
            if item.is_page:
                if item.previous_page:
                    item.previous_page.next_page = item.next_page
                if item.next_page:
                    item.next_page.previous_page = item.previous_page
                item.previous_page = None
                item.next_page = None
            # it's a section
            else:
                self._connect_pages(item.children)
                if self._temp_page:
                    self._temp_page.next_page = None
                    self._temp_page = None
            # is top level?
            if item.parent:
                item.parent.children.remove(item)
            else:
                self._nav_items.remove(item)

        self._connect_pages(self._nav_items)
        if self._temp_page:
            self._temp_page.next_page = None
            self._temp_page = None

    def set_nav(self):
        self._organize_nav(self._nav_items)
        self._organize_pages()
