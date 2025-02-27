from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """用於 Django 模板，安全地從字典中獲取鍵值"""
    return dictionary.get(key, [])
