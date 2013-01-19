import factory
from datetime import timedelta
from datetime import datetime
from competition.models import (Competition, Game, Avatar, Team,
                                Score, Organizer, OrganizerRole,
                                Registration, RegistrationQuestion,
                                RegistrationQuestionChoice,
                                RegistrationQuestionResponse)


def name_generator(formatted_string):
    """A generator that adds an incrementing integer to a string
    """
    for i in range(1, 10000):
        yield formatted_string % i

def now(_):
    return datetime.now()

def later(_):
    return datetime.now() + timedelta(hours=12)


class CompetitionFactory(factory.Factory):
    FACTORY_FOR = Competition
        
    name = factory.Iterator(name_generator("MegaMinerAI: %d"))
    start_time = factory.LazyAttribute(now)
    end_time = factory.LazyAttribute(later)
    cost_per_team = "24.00"
    min_num_team_members = 1
    max_num_team_members = 3
    description = "This is the best MegaMinerAI ever yay!"

class GameFactory(factory.Factory):
    FACTORY_FOR = Game


class AvatarFactory(factory.Factory):
    FACTORY_FOR = Avatar


class TeamFactory(factory.Factory):
    FACTORY_FOR = Team


class ScoreFactory(factory.Factory):
    FACTORY_FOR = Score


class OrganizerFactory(factory.Factory):
    FACTORY_FOR = Organizer


class OrganizerRoleFactory(factory.Factory):
    FACTORY_FOR = OrganizerRole


class RegistrationFactory(factory.Factory):
    FACTORY_FOR = Registration


class RegistrationQuestionFactory(factory.Factory):
    FACTORY_FOR = RegistrationQuestion


class RegistrationQuestionChoiceFactory(factory.Factory):
    FACTORY_FOR = RegistrationQuestionChoice


class RegistrationQuestionResponseFactory(factory.Factory):
    FACTORY_FOR = RegistrationQuestionResponse
