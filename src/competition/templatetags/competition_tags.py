from django import template

from ..models import Competition

register = template.Library()


@register.inclusion_tag('competition/_competitions_registered.html',
                        takes_context=True)
def competitions_registered(context):
    user = context['user']
    competitions = Competition.objects.user_registered(user)
    return {'competitions': competitions}
