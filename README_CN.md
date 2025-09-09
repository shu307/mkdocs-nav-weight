## mkdocs-nav-weight

这个插件是一个简单的 [MkDocs](https://www.mkdocs.org/) 插件，它允许您通过在文档的 [Markdown 元数据（或 front-matter）](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data) 中添加额外的关键词来控制页面排序、章节排序和页面在导航栏中的可见性。

该插件模拟了其他静态网站生成器（如 Hugo）中的功能，提供了一种更自然、更“Markdown 化”的方式来控制 MkDocs 网站中页面的顺序。页面顺序通过 `weight` 关键词设置，该关键词控制文档与其所在文件夹中其他文档的相对顺序。

**YAML**

```
title: 入门 - 某个主题
description: 关于某个重要事项的第一个教程
weight: 1
```

您希望出现在上述页面之后的页面将具有更高的 `weight` 值。

**YAML**

```
title: 后续步骤 - 某个主题
description: 需要排在第一个教程之后的第二个教程
weight: 2
```

附加关键词（如下所述）控制页面在导航栏中的可见性、章节名称以及章节出现的顺序。

该插件在构建过程中会读取每个 Markdown 文件中的关键词，因此可能会增加一些构建性能开销。

---

## 用法

该插件在 [MkDocs Markdown 元数据](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data) 中启用了四个额外的关键词。

| **关键词**    | **数据类型** | **默认值** | **适用范围**          | **描述**                                                                                                                                                                                                                                                                                                     |
| ---------------- | --------------- | ------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `weight`   | `number`  | `0`     | 所有 Markdown 文件     | 控制页面在文件夹中的相对顺序，页面按权重从低到高排序。对于`index.md`文件，其权重用于控制章节（文件夹）的排序。如果页面不包含`weight`关键词，它将被赋予默认值`0`，或者`mkdocs.yml`文件中`default_page_weight`属性设置的值（如下所述）。                                                    |
| `headless` | `bool`    | `false` | 所有 Markdown 文件     | 控制页面是否在导航栏中隐藏。隐藏的页面仍然可以通过直接访问其 URL 来访问。对于`index.md`文件，该关键词控制章节（文件夹）在导航栏中的可见性。                                                                                                                                                               |
| `retitled` | `bool`    | `false` | 仅限`index.md`文件 | 表示章节应使用`index.md`文件中的`title`值，而不是文件夹名称。这允许您将章节重命名为比典型目录名更友好的名称。如果`mkdocs.yml`文件中的`section_renamed`属性（如下所述）设置为`true`，则此选项将被忽略。在这种情况下，所有页面都将使用其各自`index.md`文件中的`title`值进行重命名。 |
| `empty`    | `bool`    | `false` | 仅限`index.md`文件 | 表示`index.md`文件不包含任何内容，只有元数据。如果设置为`true`，`index.md`文件将不会出现在导航栏中，仅用于提供章节元数据（例如章节的`weight`和`title`）。                                                                                                                                 |

---

## 安装

使用 `pip` 进行安装：

**Shell**

```
pip install mkdocs-nav-weight
```

将以下几行添加到 `mkdocs.yml` 中：

**YAML**

```
plugins:
  - search
  - mkdocs-nav-weight
```

---

## 配置选项

在 `mkdocs.yml` 中进行配置：

**YAML**

```
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

| **参数**                 | **默认值** | **描述**                                                                                                                                                                                           |
| --------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `section_renamed`     | `false` | 当为`true`时，章节名称将使用其`index.md`页面的`title`，而不是文件夹名称。例如，您可能有一个名为`csharp`的文件夹，但希望章节名称为`C#`。将此参数设置为`true`即可启用此行为。 |
| `index_weight`        | `-10`   | 用于`index.md`页面的`weight`值，以确保它始终在文件夹中排在首位。文件夹中的所有其他页面都应具有大于此值的`weight`值（以便它们在`index.md`页面之后列出）。                            |
| `default_page_weight` | `0`     | 分配给每个页面的默认权重（当页面不包含`weight`值时）。如果您希望没有`weight`值的页面排在最后，请将此值设置为一个较大的数字（例如：1000）。                                                  |
| `reverse`             | `false` | 默认情况下，页面按权重值从低到高排序。将此值设置为`true`将按从高到低的顺序排序。                                                                                                                |
| `headless_included`   | `false` | 一个选项，用于控制是否应将`headless`页面包含在`nav.pages`中，该属性供一些插件使用，例如：[mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin)。                  |
| `warning`             | `true`  | 控制当在 Markdown 元数据中检测到无效值时是否发送`Warning`警告。                                                                                                                                 |
