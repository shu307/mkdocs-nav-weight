# mkdocs-nav-weight

> **A simple mkdocs plugin, enable to sort nav by setting "weight" in markdown metadata** </br>
> **Not sure if it works (at least it does in my local docs).**</br>
> **mkdocs get `nav` first, and then reads markdown resource to `page`. This plugin try to read markdown resource before the mkdocs do it, so using this plugin may introduce performance problems**
## How it works
Get the `weight` of each child of the folder (`section`): 
- if it is a `page`, try to get its value, if the value is invalid, return 0;
- if it is a folder (`section`), then try to get the value from the child of its children wich is a `page` and `isindex=true`, if it is not found or the value is invalid, returns 0. </br>
- sort these children by `weight`.

Recursively all folders starting from `docs`
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

## Example
Markdown metadata like this:
```csharp
foo.md
---
title: foo
weight: 4
...
---
```

In the following, it is simply expressed as:
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

