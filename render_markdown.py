import markdown
import bleach

from bleach_whitelist import markdown_tags, markdown_attrs, all_styles
from mdx_gfm import GithubFlavoredMarkdownExtension


def markdown_to_html(raw_markdown):
    source = make_unicode(raw_markdown)
    html = markdown.markdown(source, extensions=[GithubFlavoredMarkdownExtension()])
    return bleach.clean(html, markdown_tags, markdown_attrs, all_styles)


def make_unicode(inp):
    if type(inp) != unicode:
        return inp.decode('utf-8')
    return inp
