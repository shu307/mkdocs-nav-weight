# mkdocs-nav-weight

[中文](./README_CN.md)

> [!NOTE]
>
> If you are looking for a suitable Markdown editor, or are using [Obsidian](https://obsidian.md/), then there is a plugin with basically the same functionality available [here](https://github.com/shu307/obsidian-nav-weight).

A simple [MkDocs](https://www.mkdocs.org/) plugin that allows page sorting, section sorting, and page visibility in the navigation to be controlled through additional keywords added to the dds  [Markdown Metadata (or front-matter)](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data) of your docs.

This plugin emulates functionality found in other static site generators like Hugo and provides a more natural, markdownic way to control the order of your pages in an MkDocs site.  Page order is set using the `weight` keyword which controls the relative order of the doc when compared to other docs in the same folder.

```yaml
title: Getting Started - Some Topic
description: A First Tutorial on Something Important
weight: 1
```

A page you want to appear after the page above would have a higher `weight` value.

```yaml
title: Next Steps - Some Topic
description: A Second tutorial that needs to come after the first
weight: 2
```

Additional keywords (described below) control the visibility of the page in the nav, the name of the section, and the order the sections appear.

This plugin will read the keywords from each markdown file during the build process and therefore may add some performance overhead on building.

## Usage

This plugin enables four additional keywords in the [MkDocs Markdown Metadata](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data).  


| **Keyword**  | **Datatype** | **Default Value**  |**Applies to**         | **Description** |
|--------------|--------------|--------------------|-----------------------|-----------------|
| `weight`     | `number`     | `0`                | All markdown files    | Controls the relative order of the page in the folder, with pages sorted from lowest weight to highest. For `index.md` files, this weight is used to order the sections (folders) at the folder level. If the `weight` keyword is not included for a page, it will be assigned a default `weight` of `0` or the value of the `default_page_weight` property set in the `mkdocs.yml` file as described below. |
| `headless`   | `bool`       | `false`            | All markdown files    | Controls if the page is hidden from the nav.  Pages hidden from the nav are still accessible by directly navigating to the URL.  For index.md files, this keyword controls the visibility of the section (folder) in the nav |
| `retitled`   | `bool`       | `false`            | `index.md` files only | Indicates that the section should use the `title` value of the `index.md` file rather than the folder name.  This allows you to rename sections into friendlier names that typical directory named.  This option is ignored if the property `section_renamed` is set to `true` in the `mkdocs.yml` file (see below).  In this case, all pages will be retitled using the `title` value in their respective `index.md` file. |
| `empty`      | `bool`       | `false`            | `index.md` files only | Indicates that the `index.md` file does not contain any content, only metadata.  If set to `true`, the `index.md` file will not appear in the nav and only be used to provide metadata about the section (such as the `weight` and `title` of the section). |

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

## Configuration Options

Configure in `mkdocs.yml`:

```yaml
plugins:
  - search
  - mkdocs-nav-weight:
      section_renamed: false
      index_weight: -10
      warning: true
      reverse: false
      headless_included: false
      default_page_weight: 1000
```

| **Parameter**        | **Default Value** | **Description**  |
|----------------------|-------------------|------------------|
| `section_renamed`    | `false`           | When `true`, the section name will use the `title` of its `index.md` page instead of the folder name.  For example, you may have a folder named `csharp` but want the name of the section to be `C#`.  Setting this parameter to `true` enables this behavior. |
| `index_weight`       | `-10`             | The `weight` value to use for the `index.md` page to ensure it's always shown first in the folder.  All other pages in the folder should have `weight` values greater than this value (so they will be listed *after* the index.md page). |
| `default_page_weight` | `0`               | The default weight assigned to each page (when the page does not contain a `weight` value).  If you want pages without a `weight` value to be sorted at the end, set this value to a high number (example: 1000). |
| `reverse`            | `false`           | By default, pages are sorted from lowest weight value to highest. Setting this value to `true` will sort pages from highest to lowest. |
| `headless_included`  | `false`           | An option to control whether `headless` pages should be included in `nav.pages` which is used by some plugins, eg: [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin). |
| `warning`   | `true` | Controls whether to send a `Warning` when invalid values are detected in markdown metadata. |