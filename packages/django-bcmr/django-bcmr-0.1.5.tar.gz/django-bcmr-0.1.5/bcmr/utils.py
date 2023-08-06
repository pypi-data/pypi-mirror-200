from bcmr.models import AuthToken


def generate_auth_token():
    a = AuthToken()
    a.save()
    return a
