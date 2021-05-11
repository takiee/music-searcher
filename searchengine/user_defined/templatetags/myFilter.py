from django import template
#声明模板对象，也称为注册过滤器
register=template.Library()
#声明并定义过滤器
@register.filter
def stessword(value):

    return value