from django import template

from ..models import Competition, Invitation

register = template.Library()


@register.inclusion_tag('competition/_competitions_registered.html',
                        takes_context=True)
def competitions_registered(context):
    user = context['user']
    competitions = Competition.objects.user_registered(user)
    return {'competitions': competitions}


@register.simple_tag(takes_context=True)
def invitation_count(context):
    user = context['user']
    return Invitation.objects.filter(receiver=user.pk).count()
