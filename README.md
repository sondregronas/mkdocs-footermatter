# mkdocs-footermatter (Work in progress..)
A plug-in to extract `author`, `created` and `updated`data from the YAML fronmatter to be rendered in a footer template.

There are no tests associated with this project (yet). Things may (*or may not*) break.

![img.png](img.png)

Inspired by https://github.com/timvink/mkdocs-git-revision-date-localized-plugin and https://github.com/ojacques/mkdocs-git-committers-plugin-2, without the need of using git logs.

This solves a problem I had when batch renaming every file inside a GitHub action which would overwrite the aforementioned logs. (Renaming `%20` to `-`)

Can be used in conjunction with the Obsidian plug-in https://github.com/beaussan/update-time-on-edit-obsidian

For now it is installed using `pip install git+https://github.com/sondregronas/mkdocs-footermatter`

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
created: 2022-04-09
updated: 2022-08-13
---
# Homepage
Alternatively:
authors: [Firstname Lastname, Author2] (comma separated)
authors: Firstname Lastname (single)
```

## Config
While there's not much customizability (in fact there is none), here is a list of the configuration options.

- `key_authors` fronmatter syntax for authors. Default: `authors`
- `key_created` frontmatter syntax for date created. Default: `created`
- `key_updated` frontmatter syntax for date updated. Default: `updated`
- `locale` ISO language code (derived from theme language/locale), fallsback to `en`
- `author_map` List of authors with 3 tuple values: `key/name | image path relative to "custom_dir" | link`
- `separator_map` separator for `author_map`. Default `|`

### Template (ignore poorly named classes)
```html
{% if footermatter_authors %}
<hr />
<div class="md-source-file">
<small>
    <div class="footnote">
        <center>
        <div class="contributors">
          <span class="md-icon last-updated-icon" title="Time since last update"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21 13.1c-.1 0-.3.1-.4.2l-1 1 2.1 2.1 1-1c.2-.2.2-.6 0-.8l-1.3-1.3c-.1-.1-.2-.2-.4-.2m-1.9 1.8-6.1 6V23h2.1l6.1-6.1-2.1-2M12.5 7v5.2l4 2.4-1 1L11 13V7h1.5M11 21.9c-5.1-.5-9-4.8-9-9.9C2 6.5 6.5 2 12 2c5.3 0 9.6 4.1 10 9.3-.3-.1-.6-.2-1-.2s-.7.1-1 .2C19.6 7.2 16.2 4 12 4c-4.4 0-8 3.6-8 8 0 4.1 3.1 7.5 7.1 7.9l-.1.2v1.8Z"></path></svg></span>
          {{ footermatter_updated }}

          <span class="md-icon last-updated-icon" title="Date of creation"> <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14.47 15.08 11 13V7h1.5v5.25l3.08 1.83c-.41.28-.79.62-1.11 1m-1.39 4.84c-.36.05-.71.08-1.08.08-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8c0 .37-.03.72-.08 1.08.69.1 1.33.32 1.92.64.1-.56.16-1.13.16-1.72 0-5.5-4.5-10-10-10S2 6.5 2 12s4.47 10 10 10c.59 0 1.16-.06 1.72-.16-.32-.59-.54-1.23-.64-1.92M18 15v3h-3v2h3v3h2v-3h3v-2h-3v-3h-2Z"></path></svg> </span>
          {{ footermatter_created }}

          <span class="md-icon last-updated-icon" title="Contributors"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"></path></svg></span>
          <span class="last-updated last-updated-authors last-updated-text">
              GitHub
          </span>
          {%- for author in footermatter_authors -%}
          <span class="contributor"><a href="{{ author[2] }}" title="{{ author[0] }}" target="_blank"><img src="{{ base_url }}/{{author[1]}}" alt="{{ author[0] }}"></a></span>
          {%- endfor -%}
        </div>
        </center>
    </div>
</small>
</div>
{% endif %}
```

### CSS
```css
.contributors{
	padding-top: 1ch;
}
.contributors img{
    border-radius:100%;
    width:1.75rem;
	margin-left: 0.5ch;
    margin-top:-3px;
    overflow:hidden;
	vertical-align: middle;
    filter: grayscale(100%);
    -webkit-filter: grayscale(100%);
	transition:.3s all;
}

.contributors img:hover {
    filter: none;
    -webkit-filter: grayscale(0);
	transition:.3s all;
}


.last-updated{
	color: var(--md-default-fg-color--light);
}

.last-updated-text{
	margin-inline: 0.5ch;
}

.last-updated-icon{
	display: inline-block;
	vertical-align: middle;
	font-size: .75rem;
	padding-bottom: 2px;
}
```
