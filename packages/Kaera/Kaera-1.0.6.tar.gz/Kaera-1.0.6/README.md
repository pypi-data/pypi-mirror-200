# Kaera

Gitlab project instatiator

Requires a config file as follow:

```yaml
---

group:
  name: mygroup
  desc: groupdesc
  img: path/to/img
  vars:
    some: vars

projects:
  - name: myproject
    desc: my project
    img: path/to/project/img
    src: https://gitlab.com/path/to/src/project/template
    labels:
      labelname: color
    boards:
      boardname:
        - labelname
    vars:
      some: vars
```

To install:

> pip install kaera

Or using this repo

> pip install -e .


To use:

> kaera myconfig.yaml --token GITLAB_TOKEN
