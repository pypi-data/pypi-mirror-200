from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status

from bcmr.auth import HeaderAuthentication
from bcmr.utils import generate_auth_token
from bcmr.serializers import *
from bcmr.filters import *
from bcmr.models import *
from bcmr.forms import *


def get_or_create_owner(auth_token_id):
    if auth_token_id:
        return AuthToken.objects.get(id=auth_token_id)
    else:
        return generate_auth_token()


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    filterset_class = TokenFilter
    filter_backends = (filters.DjangoFilterBackend, )
    authentication_classes = (HeaderAuthentication, )
    serializer_class = EmptySerializer
    serializer_classes = {
        'create': CashTokenSerializer,
        'list': RegistryIdentitySerializer,
        'update': CashTokenSerializer,
        'partial_update': CashTokenSerializer,
        'retrieve': RegistryIdentitySerializer
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)            
        serializer.validated_data['owner'] = get_or_create_owner(request.META.get(settings.AUTH_HEADER))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


@method_decorator(name='main', decorator=swagger_auto_schema(responses={200: BcmrRegistrySerializer}))
class RegistryViewSet(viewsets.GenericViewSet):
    queryset = Registry.objects.filter(active=True)
    # filterset_class = RegistryFilter
    # filter_backends = (filters.DjangoFilterBackend, )
    # authentication_classes = (HeaderAuthentication, )
    serializer_class = EmptySerializer
    # serializer_classes = {
    #     # 'create': RegistrySerializer,
    #     'list': RegistrySerializer,
    #     # 'update': RegistrySerializer,
    #     # 'partial_update': RegistrySerializer,
    #     'retrieve': BcmrRegistrySerializer
    # }

    @action(methods=['GET'], detail=False)
    def main(self, request, *args, **kwargs):
        obj = Registry.objects.filter(active=True).order_by('-latest_revision').first()
        serializer = BcmrRegistrySerializer(obj)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)            
    #     serializer.validated_data['owner'] = get_or_create_owner(request.META.get(settings.AUTH_HEADER))
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # @swagger_auto_schema(responses={200: BcmrRegistrySerializer})
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     instance.latest_revision = timezone.now()
    #     instance.save()

    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     bcmr = BcmrRegistrySerializer(instance)
    #     return Response(bcmr.data)

    # def get_serializer_class(self):
    #     if not isinstance(self.serializer_classes, dict):
    #         raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

    #     if self.action in self.serializer_classes.keys():
    #         return self.serializer_classes[self.action]
    #     return super().get_serializer_class()

 
def create_token(request):
    submitted = False
    message = ''
    owner = ''

    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict.lists())

        category = data['category'][0]
        name = data['name'][0]
        description = data['description'][0]
        symbol = data['symbol'][0]
        decimals = int(data['decimals'][0])
        auth_token = data['auth_token'][0]
        icon = data['icon'][0]
        
        if Token.objects.filter(category=category).exists():
            message = 'Token category already exists!'
        else:
            try:
                owner = get_or_create_owner(auth_token)
                token = Token(
                    category=category,
                    name=name,
                    description=description,
                    symbol=symbol,
                    decimals=decimals,
                    owner=owner,
                    icon=icon
                )
                token.save()
                message = 'Token added!'
            except:
                message = 'Invalid auth token!'

        submitted = True

    context = {
        'form': TokenForm(),
        'submitted': submitted,
        'message': message,
        'owner': owner if type(owner) is str else owner.id
    }
    return render(request, 'bcmr/create_token.html', context)
