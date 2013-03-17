from django import template

from ..models import Competition, Invitation, Team

register = template.Library()


@register.inclusion_tag('competition/_competitions_registered.html',
                        takes_context=True)
def competitions_registered(context):
    user = context['user']
    competitions = Competition.objects.user_registered(user)
    return {'competitions': competitions}


@register.filter
def has_unread_invitations(user):
    return Invitation.objects.filter(receiver=user.pk, read=False).exists()


@register.simple_tag(takes_context=True)
def unread_invitation_count(context):
    user = context['user']
    return Invitation.objects.filter(receiver=user.pk, read=False).count()


class TeamNode(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def render(self, context):
        user = context['user']
        context[self.variable_name] = Team.objects.invitable(user)
        return ''


@register.tag
def invitable_teams(parser, token):
    try:
        contents = token.split_contents()
        _tag_name, _as, variable_name = contents
    except AssertionError:
        msg = "%r tag requires one argument" % contents[0]
        raise template.TemplateSyntaxError(msg)

    return TeamNode(variable_name)


@register.filter
def get_item(obj, arg):
    try:
        return obj[arg]
    except (KeyError, TypeError):
        return ''
