from ckan.common import _, c
from ckan.plugins import toolkit


def check_administrator(func):
    def wrapper(*args, **kwargs):
        if c.userobj is None or c.userobj.sysadmin is None:
            toolkit.abort(
                404,
                _(
                    'The requested URL was not found on the server. If you entered the'
                    ' URL manually please check your spelling and try again.'
                ),
            )
        else:
            return func(*args, **kwargs)

    return wrapper
