# mkdocs-footermatter (Work in progress..)
A plug-in to extract `author`, `created` and `updated` data from the YAML fronmatter to be rendered in a footer template.

There are no tests associated with this project (yet). Things may (*or may not*) break.

![img.png](img.png)

Inspired by https://github.com/timvink/mkdocs-git-revision-date-localized-plugin and https://github.com/ojacques/mkdocs-git-committers-plugin-2, without the need of using git logs.

This solves a problem I had when batch renaming every file inside a GitHub action which would overwrite the aforementioned logs. (Renaming `%20` to `-`)

Can be used in conjunction with the Obsidian plug-in https://github.com/beaussan/update-time-on-edit-obsidian

For now it is installed using `pip install git+https://github.com/sondregronas/mkdocs-footermatter@main`

## Usage
```yaml
plugins:
  - search
  - footermatter:
      author_map:
        - Firstname Lastname | assets/img/firstname.png | https://github.com/firstnamelastname
        - Author2 | <path from "custom_dir"> | htts://github.com/author2
```

### Example frontmatter
```markdown
---
title: Homepage
aliases: [Home,]
authors:
  - Firstname Lastname
  - Author2
created: 2022-04-09 08:52:19
updated: 2022-08-13 12:18:05
---
# Homepage
```

## Config
While there's not much customizability (in fact there is none), here is a list of the configuration options.

- `key_authors` fronmatter syntax for authors. Default: `authors`
- `key_created` frontmatter syntax for date created. Default: `created`
- `key_updated` frontmatter syntax for date updated. Default: `updated`
- `locale` [ISO language code]((https://github.com/hustcc/timeago/tree/master/src/timeago/locales)), fallbacks to theme language or `en` 
- `date_format` What format to use for the dates, see below for options. Default: `timeago`
- `author_map` List of authors with attribute values: `name | img (path relative to "custom_dir") | url`
- `separator_map` separator for `author_map`. Default `|`
- `default_author_img` fallback image if missing from `author_map`. Default `https://ui-avatars.com` (See template for details)
- `default_author_url` fallback url if missing from `author_map`. Default: `/`

### Date formats
- `timeago` - a readable, relative date format. Note: values is static and only changes after building your docs.

### Template
An example setup can be seen in the `overrides` folder, including some css styling and an example `main.html`

Relevant attributes:
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
