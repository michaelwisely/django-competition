from competition.models import Competition, Game, GameScore
import random
import json

# from johnny.cache import enable
# enable()

from django.contrib.auth.models import User

print User

import django
print django


game_data = {
    'gamelog_url': 'http://placekitten.com/g/200/300',
    'api_url': None,
    'status': 'Complete',
    'winner': {},
    'loser': {},
    'game_data': []
}

score_data = {
    'output_url': 'http://placekitten.com/g/300/300',
    'version': '',
}


def run():
    c = Competition.objects.get(name__icontains="space")
    teams = list(c.team_set.all())

    c.game_set.all().delete()

    for _ in range(25):
        scores = (random.randint(0, 1) for _ in xrange(2))
        results = zip(random.sample(teams, 2), scores)

        game_data['winner']['name'] = max(results, key=lambda x: x[1])[0].slug
        game_data['loser']['name'] = min(results, key=lambda x: x[1])[0].slug

        game_data['game_data'] = [{'name': {'name': x.slug}, 'version': 'myversion'}
                                  for x, _ in results]

        g  = Game.objects.create(competition=c,
                                 extra_data=json.dumps(game_data))
        print "Created game {}".format(g.id)

        for player, score in results:
            s = GameScore.objects.create(game=g,
                                         team=player,
                                         score=score,
                                         extra_data=json.dumps(score_data))
            print "\tCreated score {}".format(s.id)
