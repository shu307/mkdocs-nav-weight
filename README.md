# mkdocs-nav-weight

> **A simple mkdocs plugin, enable to sort nav by setting "weight" in markdown metadata** </br>
> **I'm only sure it's runnable, not sure if it works (at least it does in my local docs). Only the compatibility of `section`, `index` and `page` has been considered.** </br>
> **mkdocs get `nav` first, and then reads markdown resource to `page`, so using this plugin means reading markdown source twice, which may introduce performance problems**

## Install


```shell
pip install mkdocs-nav-weight
```

`mkdocs.yml`

```yaml
plugins:
  - search
  - mkdocs-nav-weight
```



## Intro
Markdown metadata like this:
> **Note, try not to forget the `space` between `weight:` and `number`, sometimes it causes bugs, I use mkdocs its own way to get metadata, and I'm not a proficient pythoner, so I don't know how to fix it.**
```csharp
foo.md
---
title: foo
weight: 4
...
---
```
In the following, it is directly expressed as:
```csharp
foo.md // 4
```

A document tree like this:
```csharp
│  bar.md // no “weight”
│  foo.md // 4
│
├─have_index_folder
│  │  another.md // 1
│  │  index.md // 3
│  │
│  └─level2
│          another.md // 1
│          bar.md  // no “weight”
│          foo.md  // 4
│
└─no_index_folder
        alone.md // 2
```
You will get a nav like this:

```c#
bar  // 0: no 'weight', default 0
No index folder  // 0: cann't find a 'index', so it's defalut 0
	alone  // 2
Have index folder  // 3: get from 'index'
	index  // 0: it's 3 but as 0 in same level
    	Level2 // 0: no index, default 0
		bar // 0
		another // 1
		foo // 4
	another  // 1
foo  // 4
```

