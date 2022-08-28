# mkdocs-nav-weight

**A simple nav auto sort  plugin for mkdocs** 

I just make sure it's runnable, don't know if it works or not

## install

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
Markdown files metadata like this:
```csharp
foo.md
---
title: foo
weight: 4 // Try not to miss the space between `weight:` and `number`, 
---		  // sometimes it causes bugs, I use mkdocs' own way to get metadata,
...		  // I'm not a skilled pythoner, so I don't know how to fix it.

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

Get nav like this:

```c#
bar  // 0
No index folder  // 0: will not get weight from 'alone', so it's defalut 0
	alone  // 2
Have index folder  // 3: get from 'Index'
	Index  // 3: but as 0 in same level
    Level2 // 0: default
    	bar // 0
    	another // 1
    	foo // 4
	another  // 1
foo  // 4
```

