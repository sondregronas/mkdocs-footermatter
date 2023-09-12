# mkdocs-footermatter (Working title)
[![Build Status](https://img.shields.io/github/actions/workflow/status/sondregronas/mkdocs-footermatter/CI.yml?branch=main)](https://github.com/sondregronas/mkdocs-footermatter/)
[![GitHub latest commit](https://img.shields.io/github/last-commit/sondregronas/mkdocs-footermatter)](https://github.com/sondregronas/mkdocs-footermatter/commit/)
[![PyPi](https://img.shields.io/pypi/v/mkdocs-footermatter)](https://pypi.org/project/mkdocs-footermatter/)
![MIT license](https://img.shields.io/github/license/sondregronas/mkdocs-footermatter)
[![codecov](https://codecov.io/gh/sondregronas/mkdocs-footermatter/branch/main/graph/badge.svg?token=N5IDI7Q4NZ)](https://codecov.io/gh/sondregronas/mkdocs-footermatter)

A plug-in to extract `authors`, `created` and `updated` data from the YAML fronmatter to be rendered in a footer template.

This solves a problem I had when batch renaming every file inside a GitHub action which would overwrite the aforementioned logs. (Renaming `%20` to `-`)

![img.png](img.png)

Inspired by [git-revision-date-localized](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin) and [mkdocs-git-committers-plugin](https://github.com/ojacques/mkdocs-git-committers-plugin-2), without the need of using git logs.

## Setup
Install the plugin using pip:

`pip install mkdocs-footermatter`

Activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - search
  - footermatter:
      author_map:
        - Firstname Lastname | assets/img/firstname.png | https://github.com/firstnamelastname
        - Author2 | <path from "custom_dir"> | htts://github.com/author2
```
> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

### Usage
Can be used in conjunction with the Obsidian plug-in [update-time-on-edit-obsidian](https://github.com/beaussan/update-time-on-edit-obsidian)

Example frontmatter:

```markdown
---
authors:
  - Firstname Lastname
  - Author2
created: 2022-04-09 08:52:19
updated: 2022-08-13 12:18:05
---
```

## Configuration options
**Fronmatter keys:**
- `key_authors` fronmatter syntax for authors. Default: `authors`
- `key_created` frontmatter syntax for date created. Default: `created`
- `key_updated` frontmatter syntax for date updated. Default: `updated`

**Locale & format:**
- `locale` language format for date_format (some options may require this to be configured, see below) fallbacks to theme language (recommended) or `en` 
- `date_format` What format to use for the dates, see below for options. Default: `date`
- `timeago_absolute` Boolean to omit the `ago` text. True: `2 days`, False: `2 days ago`. Default: `True`

**Author rendering options:**
- `author_map` List of authors mapped image and url values: `name | img (path relative to "custom_dir" or url) | url/website`
- `separator_map` separator for `author_map`. Default `|`
- `default_author_img` fallback image if missing from `author_map`. Default `https://ui-avatars.com` (See template for details)
- `default_author_url` fallback url if missing from `author_map`. Default: `/`

## Date formats
Note: values are static and only change when re-building your docs. All formats are localized using the [Pendulum](https://pendulum.eustace.io/) package
- `timeago` (2 hours ago) - a readable, relative date format.
- `date` (January 1. 2022) - simple date format (`LL`).
- `datetime` (January 1. 2022 12:00 PM) - same as date, but with added timestamp (`LLL`)
- For custom formats just pass [a valid pendulum string format](https://pendulum.eustace.io/docs/#tokens). Example: `MMMM YYYY` = January 2022

## Template
An example setup can be seen in the [overrides](https://github.com/sondregronas/mkdocs-footermatter/tree/main/overrides) folder, including some css styling and an example [main.html](https://github.com/sondregronas/mkdocs-footermatter/blob/main/overrides/main.html)

Relevant context values:
```yaml
{{ footermatter_updated }}
{{ footermatter_created }}
{%- for author in footermatter_authors -%}
    {{ author.name }}
    {{ author.img }} 
    {{ base_url }}/{{ author.img }}
    {{ author.url }}
{%- endfor -%}
```
