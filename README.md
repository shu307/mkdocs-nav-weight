# mkdocs-nav-weight

**A simple mkdocs plugin, enables to organize Navigation in a more markdownic way.** 

> **This plugin tries to read markdown resources before mkdocs, which may add some performance overhead on building.**

## Usage

Three additional keys can be configured in Markdown Metadata ( also known as "front-matter", see [metadata](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)):

- `weight: number`
    - **value: number, eg: `-1`, `2.3` ..., if unset, it goes `0`**.
    - like weight in Hugo but has some differences, used for ordering your sections/pages. Lower weight gets higher precedence. So content with lower weight will come first. 
    - **`weight` in an `index` will be offered to its parent `section`**, there is a fixed value for itself, and the value is configurable, see: [index_weight](#index_weight).

- `headless: bool`
    - **value: bool, `true` or `false`, if unset, it goes `false`**.
    - like headless in Hugo, pages/sections with `headless: true` will be hidden from nav, but these contents will still be rendered and accessible via URL.
    - **`headless` in an `index` will be offered to its parent `section`, too**

- `section: bool`
    - **value: bool, `true` or `false`, if unset, it goes `false`**.
    - For `index` only.
    - If there is an `index` only used to offer metadata for its parent `section` and without any meaningful content, setting `section` to `true` can help you to hide this `index` itself.



## Installation

Install with `pip`:


```shell
pip install mkdocs-nav-weight
```

Add the following lines to `mkdocs.yml`

```yaml
plugins:
  - search
  - mkdocs-nav-weight
```

## Options

Setting in `mkdocs.yml`:

```yaml
plugins:
  - search
  - mkdocs-nav-weight:
      section_renamed: false
      index_weight: -10
      warning: true
      reverse: false
```

### `section_renamed`

Default: `false`:

- If `true`, section name will use the `title` of its `index` instead of the folder name. 

- For compatibility we have to name a folder like "C#" as "CSharp", but what we actually want is "C#" , that's what this option does

### `index_weight`

Default: `-10`:

- The `weight` value for `index` itself, to ensure it's always the first at the same level

### `warning`

Default: `true`:

- Controls whether to send a `Warning` when invalid values are detected in markdown metadata

### `reverse`

- If `true`, sort nav by `weight` from largest to smallest.
