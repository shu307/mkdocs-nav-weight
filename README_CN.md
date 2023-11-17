# mkdocs-nav-weight

**一个简单的 mkdocs 插件，以更 markdown 的方式组织导航。** 

> **该插件尝试在 mkdocs 之前读取 markdown 资源，会有一些额外性能消耗。**

## 使用

可在 Markdown Metadata ( 也叫 "front-matter", 见 [metadata](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)) 中配置的额外4个键值对。

- `weight: number`
    - **值: number, 如 `-1`, `2.3` ..., 未设置，则为 `0`**.
    - 类似于 Hugo 中的 weight ，但有一些差异，用于对 section 和 page 排序。  weight 越低，顺序越靠前。
    - **`index` 中的 `weight` 会被提供给其父 `section`**, 其本身有一个可配置的固定值，见: [`index_weight`](#index_weight).
    - **weight 的作用域只在同文件夹**

- `headless: bool`
    - **值: bool, `true` or `false`, 未设置，则为 `false`**.
    - 和 Hugo 中的 headless 一样，带有 `headless: true` 的 page 和 section 将从导航中分离，但仍会被渲染，能通过 URL 访问。
    - **`index` 中的 `headless` 同样会被提供给其父 `section`**.

**仅供 `index` :**

- `retitled: bool`
    - **值: bool, `true` or `false`, 未设置，则为 `false`**.
    - 一个 metadata 版本的 [`section_renamed`](#section_renamed), 仅将此 `index`的标题提供给其父 `section`, **只在 `section_renamed` 是 `false` 时起效**.

- `empty: bool`
    - **值: bool, `true` or `false`, 未设置，则为 `false`**.
    - 如果此 `index` 仅用于给其父 `section` 提供 metadata, 而没有任何实际内容, 设置 `empty` 为 `true` 将会从导航中分离此 `index` .

## 安装

使用 `pip` 安装:


```shell
pip install mkdocs-nav-weight
```

添加下列行到 `mkdocs.yml`

```yaml
plugins:
  - search
  - mkdocs-nav-weight
```

## 选项

在 `mkdocs.yml` 中配置:

```yaml
plugins:
  - search
  - mkdocs-nav-weight:
      section_renamed: false
      index_weight: -10
      warning: true
      reverse: false
      headless_included: false
```

#### `section_renamed`

默认: `false`:

- 如果为 `true`, section 会使用其子 `index` 的 `title` 而不是文件夹名. 

- 出于兼容性，我们无法使用类似 "C#" 的包含url非法字符的文件夹命名，而只能采取一些不太和谐的命名，该选项用于覆盖所有 `section` 的标题(文件夹名).

#### `index_weight`

默认: `-10`:

- `index` 自身的 `weight`，确保其位于同级别首位(或末位?).

#### `warning`

默认: `true`:

- 检测到 metadata 值类型不正确时，是否发送警告

#### `reverse`

默认: `false`:

- 如果设置为 `true`, 排序时 `weight` 越大越靠前.

#### `headless_included`

默认: `false`:

- 控制 `headless` 是否应被包含在 `nav.pages` 中，此列表被一些插件使用, 如: [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin).

- 如果设置为 `true`,  `nav.pages` 将会包含 `headless` 页面.