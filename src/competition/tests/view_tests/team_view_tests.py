from competition.models.team_model import Team
from competition.models.competition_model import Competition
from competition.tests.utils import FancyTestCase


class TeamViewsTest(FancyTestCase):
    fixtures = ['competition_test_data.yaml',
                'team_test_data.yaml']

    def setUp(self):
        self.space = Competition.objects.get(slug__contains="space")
        self.space_teams = Team.objects.filter(competition=self.space)

        self.galapagos = Competition.objects.get(slug__contains="galapagos")
        self.galapagos_teams = Team.objects.filter(competition=self.galapagos)

    
