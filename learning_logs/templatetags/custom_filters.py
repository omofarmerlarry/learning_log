from django import template
import markdown

register=template.Library()

@register.filter(name='markdown_format')
def markdown_format(text):
    return markdown.markdown(text, extensions=['extra', 'codehilite'])