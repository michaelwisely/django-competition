from django.dispatch import Signal

from functools import wraps
import inspect


def disable_for_loaddata(signal_handler):
    """Disables a signal when a fixture is being loaded

    Fix from https://code.djangoproject.com/ticket/8399
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == 'loaddata':
                return
        signal_handler(*args, **kwargs)
    return wrapper


#: Signal to be sent whenever a user's registration is deactivated
registration_deactivated = Signal()
