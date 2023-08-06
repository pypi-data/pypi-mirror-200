import re

from markdown2 import markdown


SINGLE_PARAGRAPH_PATTERN = re.compile(r'^<p>((?:(?!<p>).)*)</p>$')
NESTED_TAG_PATTERN = re.compile(r'<p>(<.*>)</p>')
EXTRAS = [
    'break-on-newline',
    'code-friendly',
    'cuddled-lists',
    'fenced-code-blocks',
    'footnotes',
    'header-ids',
    'markdown-in-html',
    'strike',
    'target-blank-links',
    'tables',
    'use-file-vars',
    'task_list']


def get_html_from_markdown(text, extras=EXTRAS):
    html = markdown(text, extras=extras).strip()
    match = SINGLE_PARAGRAPH_PATTERN.match(html)
    if match:
        html = match.group(1)
    return NESTED_TAG_PATTERN.sub(lambda _: _.group(1), html)
