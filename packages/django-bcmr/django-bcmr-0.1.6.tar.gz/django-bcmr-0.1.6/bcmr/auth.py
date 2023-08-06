from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated

from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from bcmr.models import *


class HeaderAuthentication(BaseAuthentication):

    def __init__(self, realm="API"):
        self.realm = realm

    def authenticate(self, request, **kwargs):
        try:
            if request.method == 'GET':
                request.user = AnonymousUser()
                return (request.user, None)

            bcmr_auth_token = request.META.get(settings.AUTH_HEADER)
            if not bcmr_auth_token:
                if request.method == 'POST':
                    request.user = AnonymousUser()
                    return (request.user, None)
                else:
                    raise NotAuthenticated(detail='BCMR authorization token required', code=403)

            auth_token = AuthToken.objects.get(id=bcmr_auth_token)
            if auth_token:
                model = request.path_info.split('/')[2]
                pk = request.path_info.split('/')[3]
                
                if pk:
                    model_obj = None
                    try:
                        if model == 'registries':
                            model_obj = Registry.objects.get(id=pk)
                        elif model == 'tokens':
                            model_obj = Token.objects.get(category=pk)
                    except:
                        pass
                        
                    if model_obj:
                        if str(model_obj.owner.id) != bcmr_auth_token:
                            raise NotAuthenticated(
                                detail='Unauthorized action: only owner can modify this data',
                                code=403
                            )

                request.user = AnonymousUser()
                return (request.user, None)
        except AuthToken.DoesNotExist as dne:
            raise NotAuthenticated(detail='Invalid auth token', code=403)
        except KeyError as ke:
            raise NotAuthenticated(detail='Client Not Found', code=403)
