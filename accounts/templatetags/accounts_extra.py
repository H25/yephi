from django import template

register = template.Library()

@register.filter
def has_relationship(obj, args):
    return obj.has_relationship(args)

@register.filter
def has_request(obj, args):
    return obj.has_request(args)

@register.filter
def has_in_favlist(obj, args):
    return obj.get_profile().has_in_favlist(args)

@register.filter
def compare_favlist(obj, args):
    return obj.compare_favlist(args)

@register.filter
def has_reviewed(obj, args):
    return obj.get_profile().has_reviewed(args)

@register.filter
def get_review(obj, args):
    return obj.get_profile().get_review(args)

@register.filter
def replace(obj, args):
    return obj.replace('%NAME%', args)