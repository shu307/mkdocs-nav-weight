# mkdocs-nav-weight

> **A simple mkdocs plugin, enable to sort nav by setting "weight" in markdown metadata** </br>
> **I'm only sure it's runnable, not sure if it works (at least it does in my local docs). Only the compatibility of `section`, `index` and `page` has been considered, but not others such as "homepage".** </br>
> **mkdocs get `nav` first, and then reads markdown resource to `page,` so using this plugin means reading markdown source twice, which may introduce performance problems**

## Install

I  don't know how to package, so let it be:

```shell
pip install git+https://github.com/shu307/mkdocs-nav-weight
```

`mkdocs.yml`

```yaml
plugins:
  - search
  - mkdocs-nav-weight
```



## Intro

A document tree like this:
```
│  bar.md
│  foo.md
│
├─have_index_folder
│  │  another.md
│  │  index.md
│  │
│  └─level2
│          another.md
│          bar.md
│          foo.md
│
└─no_index_folder
        alone.md
```
Markdown metadata like this:
> **Note, try not to forget the `space` between `weight:` and `number`, sometimes it causes bugs, I use mkdocs its own way to get metadata, and I'm not a proficient pythoner, so I don't know how to fix it.**
```csharp
foo.md
---
title: foo
weight: 4
---
...

bar.md  // no "weight", default = 0
---
title: bar
---
...

index.md 
---
title: index
weight: 3
---
...

another.md
---
title: another
weight: 1
---
...

alone.md
---
title: alone
weight: 2
---
```

Get a nav like this:

```c#
bar  // 0: no 'weight', default 0
No index folder  // 0: will not get weight from 'alone', so it's defalut 0
	alone  // 2
Have index folder  // 3: get from 'index'
	index  // 3: but as 0 in same level
    	Level2 // 0: no index, default 0
		bar // 0
		another // 1
		foo // 4
	another  // 1
foo  // 4
```

