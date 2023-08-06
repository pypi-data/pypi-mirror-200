from django_filters import rest_framework as filters

from bcmr.models import *


# class RegistryFilter(filters.FilterSet):
#     class Meta:
#         model = Registry
#         fields = (
#             'owner',
#         )


class TokenFilter(filters.FilterSet):
    class Meta:
        model = Token
        fields = (
            'owner',
            'is_nft',
        )
