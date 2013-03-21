from django.contrib import admin
from django.db.models import Q

from competition.models.avatar_model import Avatar
from competition.models.competition_model import Competition
from competition.models.game_model import Game, GameScore
from competition.models.organizer_model import Organizer
from competition.models.organizer_model import OrganizerRole
from competition.models.registration_model import Registration
from competition.models.registration_model import RegistrationQuestion
from competition.models.registration_model import RegistrationQuestionChoice
from competition.models.registration_model import RegistrationQuestionResponse
from competition.models.team_model import Team
from competition.models.invitation_model import Invitation


##############################################################################
#
# Inline Admins
#
##############################################################################

class InlineTeamAdmin(admin.TabularInline):
    model = Team
    extra = 0
    max_num = 0
    fields = ('created', 'avatar', 'name', 'paid',
              'time_paid', 'eligible_to_win')
    readonly_fields = ('avatar', 'created')
    ordering = ('created',)


class InlineGameAdmin(admin.TabularInline):
    model = Game
    extra = 0
    fields = ('id', 'start_time', 'end_time')
    readonly_fields = ('id',)


class InlineOrganizerAdmin(admin.TabularInline):
    model = Organizer
    extra = 0
    fields = ('user', 'role')
    filter_horizontal = ('role',)


class InlineRegistrationAdmin(admin.TabularInline):
    model = Registration
    fields = ('user', 'signup_date',)
    readonly_fields = ('user', 'signup_date',)


class InlineRegistrationQuestionAdmin(admin.StackedInline):
    model = RegistrationQuestion


class InlineRegistrationQuestionChoiceAdmin(admin.StackedInline):
    model = RegistrationQuestionChoice


class InlineResponseAdmin(admin.TabularInline):
    extra = 0
    max_num = 0
    supported_question_types = ('SA', 'SC', 'MC', 'AB')

    def queryset(self, request):
        qs = super(InlineResponseAdmin, self).queryset(request)
        supported = self.supported_question_types
        queries = [Q(question__question_type=t) for t in supported]
        query = reduce(lambda x, y: x | y, queries)
        return qs.filter(query)


class InlineShortAnswerResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'text_response')
    readonly_fields = ('question', 'text_response')
    supported_question_types = ('SA',)


class InlineMultipleChoiceResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'choices')
    readonly_fields = ('question', 'choices')
    supported_question_types = ('SC', 'MC')


class InlineAgreementResponseAdmin(InlineResponseAdmin):
    model = RegistrationQuestionResponse
    fields = ('question', 'agreed')
    readonly_fields = ('question', 'agreed')
    supported_question_types = ('AB',)


##############################################################################
#
# Model Admins
#
##############################################################################

class AvatarAdmin(admin.ModelAdmin):
    readonly_fields = ('image_height', 'image_width',
                       'thumbnail', 'thumbnail_height', 'thumbnail_width')


class CompetitionAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    list_display = ('name', 'is_open', 'is_running',
                    'start_time', 'end_time')
    list_filter = ('is_open', 'is_running', 'start_time', 'end_time')
    prepopulated_fields = {"slug": ("name",)}
    inlines = (InlineOrganizerAdmin,)


class GameAdmin(admin.ModelAdmin):
    list_display = ('pk','competition','game_id')
    list_filter = ('competition')
    pass

class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('pk','game','team','score')
    list_filter = ('team',)
    raw_id_fields = ('game',)

class OrganizerRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('competition', 'user')
    filter_horizontal = ('role',)


class RegistrationAdmin(admin.ModelAdmin):
    inlines = (InlineShortAnswerResponseAdmin,
               InlineMultipleChoiceResponseAdmin,
               InlineAgreementResponseAdmin)
    list_display = ('user', 'competition', 'signup_date', 'active')
    list_filter = ('signup_date', 'active')


class RegistrationQuestionAdmin(admin.ModelAdmin):
    inlines = (InlineRegistrationQuestionChoiceAdmin,)
    list_display = ('question_type', 'question')
    list_filter = ('question_type',)


class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    list_display = ('name', 'competition', 'created', 'paid')
    list_filter = ('competition', 'paid', 'created')
    prepopulated_fields = {"slug": ("name",)}

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'team', 'sent', 'read')
    list_filter = ('sent', 'read')


admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameScore, GameScoreAdmin)
admin.site.register(OrganizerRole, OrganizerRoleAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(RegistrationQuestion, RegistrationQuestionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Invitation, InvitationAdmin)
