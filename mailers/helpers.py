def format_bookmark(bookmark):
    bookmark_f = """\
<div class="bookmark" style="margin-bottom:4px">
  <h4 style="margin-bottom:4px">
    <a href="{}">{}</a>
  </h4>
  <div class="tags">
    {}
  </div>
  <div class="meta">
    {}
  </div>
</div>"""

    return bookmark_f.format(bookmark.url,
                             bookmark.title,
                             format_tags(bookmark),
                             format_meta(bookmark))


def format_tags(bookmark):
    tag_blocks = [format_tag(bookmark, tag) for tag in bookmark.tags]
    return ', '.join(tag_blocks)


def format_tag(bookmark, tag):
    tag_f = '<a href="{}">{} ({})</a>'
    return tag_f.format(bookmark.tag_to_url(tag), tag.name, tag.count)


def format_meta(bookmark):
    meta_f = '<span>{}</span> &bull; <a href="{}">{}</a>'
    return meta_f.format(bookmark.created_at, bookmark.service_url, bookmark.service_url)
