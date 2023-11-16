import logging
from numbers import Number
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation, Section, Link

log = logging.getLogger("mkdocs.plugins")

# common strings
SECTION_RENAMED = "section_renamed"
INDEX_WEIGHT = "index_weight"
WARNING = "warning"
REVERSE = "reverse"
HEADLESS_INCLUDED = "headless_included"
WEIGHT = "weight"
HEADLESS = "headless"
RETITLED = "retitled"
EMPTY = "empty"


class NavSetter():
    def __init__(self, nav: Navigation, config, mkdocs_config) -> None:
        # options
        self.is_section_renamed = config[SECTION_RENAMED]
        self._index_weight = config[INDEX_WEIGHT]
        self._is_warning = config[WARNING]
        self._is_reverse = config[REVERSE]
        self._is_headless_included = config[HEADLESS_INCLUDED]

        # mkdocs
        self.nav = nav
        self.mkdocs_config = mkdocs_config

        # utils
        self._meta_defaults = dict(
            WEIGHT=0,
            RETITLED=False,
            EMPTY=False,
            HEADLESS=False
        )
        """fallback for unset or invalid value"""

        self._meta_types = dict(
            WEIGHT=Number,
            RETITLED=bool,
            EMPTY=bool,
            HEADLESS=bool
        )
        """valid types for values"""

        self._section_weights = {}
        """"section weights cache dict"""

        self._empty_items = []
        """"empty indexes"""

        self._headless_items = []
        """headless list is needed later."""

    def _get_meta(self, key: str, page: Page) -> Number | bool:
        result = self._meta_defaults[key]

        meta = page.meta
        if key in meta.keys():
            if isinstance(meta[key], self._meta_types[key]):
                result = meta[key]
            # option: "warning"
            elif self._is_warning:
                log.warning(
                    f"[mkdocs-nav-weight]: Invaild value for \"{key}\" in {page}, setting to \"{result}\"")

        return result

    def _get_weight(self, item: Page | Section | Link) -> Number:
        result = 0

        if item.is_page:
            result = self._index_weight if item.is_index else self._get_meta(
                WEIGHT,  item)
        if item.is_section:
            result = self._section_weights[item]

        return result

    def _sort_items(self, items: list) -> Number:
        parent_weight = 0

        for item in items:
            if item.is_section:
                weight = self._sort_items(item.children)
                self._section_weights[item] = weight
            elif item.is_page:
                item.read_source(self.mkdocs_config)
                # normal page
                if not item.is_index:
                    if self._get_meta(HEADLESS,  item):
                        self._headless_items.append(item)
                # index, but not a top level "index" -- homepage
                elif item.parent:
                    parent_weight = self._get_meta(WEIGHT, item)
                    # option: "section_renamed"
                    if self.is_section_renamed or self._get_meta(RETITLED, item):
                        item.parent.title = item.title
                    if self._get_meta(EMPTY,  item):
                        self._empty_items.append(item)
                    if self._get_meta(HEADLESS_INCLUDED, item):
                        self._headless_items.append(item.parent)

        items.sort(key=self._get_weight, reverse=self._is_reverse)

        return parent_weight

    def _get_first_page(self, items: list) -> Page | None:
        for item in items:
            if item.is_page:
                return item
            if item.is_section:
                return self._get_first_page(item.children)

    def _do_connection_rec(self, items: list, temp_page: Page) -> Page:
        for item in items:
            if item.is_page:
                item.previous_page = temp_page
                temp_page.next_page = item
                temp_page = item
            elif item.is_section:
                temp_page = self._do_connection_rec(
                    item.children, temp_page)

        return temp_page

    def _do_connection(self, items: list) -> None:
        first_page = self._get_first_page(items)

        if first_page:
            last_page = self._do_connection_rec(items, first_page)
            first_page.previous_page = None
            last_page.next_page = None

    def _do_headless(self, item: Page | Section) -> None:
        # page
        if item.is_page:
            if item.previous_page:
                item.previous_page.next_page = item.next_page
                item.previous_page = None
            if item.next_page:
                item.next_page.previous_page = item.previous_page
                item.next_page = None
        # section
        elif item.is_section:
            self._do_connection(item.children)

        # is top level?
        if item.parent:
            item.parent.children.remove(item)
        else:
            self.nav.items.remove(item)

    def _handle_items(self) -> None:
        # isolate items
        for item in self._empty_items:
            self._do_headless(item)
        for item in self._headless_items:
            self._do_headless(item)

        # connect normal items
        self._do_connection(self.nav.items)

    def _get_nav_pages(self, items: list) -> list:
        pages = []

        for item in items:
            if item.is_page:
                pages.append(item)
            elif item.is_section:
                pages.extend(self._get_nav_pages(item.children))

        return pages

    def set_nav(self) -> Navigation:
        # nav_items
        self._sort_items(self.nav.items)
        self._handle_items()

        # nav_pages
        self.nav.pages = self._get_nav_pages(self.nav.items)
        if self._is_headless_included:
            self.nav.pages.extend(self._get_nav_pages(self._headless_items))

        return self.nav
