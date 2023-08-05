from rest_framework import serializers

from django.conf import settings

from bcmr.models import *


class EmptySerializer(serializers.Serializer):
    pass


class CashTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
            'id',
            'category',
            'name',
            'symbol',
            'description',
            'decimals',
            'icon',
            'nft_description',
            'nft_types',
            'status',
            'date_created',
            'owner',
        )
        read_only_fields = (
            'id',
            'date_created',
            'owner',
        )


class RegistryIdentitySerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    uris = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = (
            'id',
            'name',
            'description',
            'time',
            'token',
            'status',
            'uris',
        )
        read_only_fields = ('id', )

    def get_time(self, obj):
        return {
            'begin': obj.date_created
        }

    def get_token(self, obj):
        result = {
            'category': obj.category,
            'symbol': obj.symbol,
            'decimals': obj.decimals 
        }

        if obj.is_nft:
            result['nfts'] = {
                'description': obj.nft_description,
                'fields': {},
                'parse': {
                    'bytecode': '',
                    'types': obj.nft_types
                }
            }
        
        return result

    def get_uris(self, obj):
        if obj.icon:
            return {
                'icon': f'{settings.DOMAIN}{obj.icon.url}'
            }
        return {}


class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = (
            'id',
            'name',
            'description',
            'tokens',
            # 'owner',
        )
        read_only_fields = (
            # 'owner',
            'id',
        )


# class NoOwnerRegistrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Registry
#         fields = (
#             'id',
#             'name',
#             'description',
#             'tokens',
#         )
#         read_only_fields = (
#             'id',
#         )


class BcmrRegistrySerializer(serializers.ModelSerializer):
    version = serializers.SerializerMethodField()
    latestRevision = serializers.SerializerMethodField()
    registryIdentity = serializers.SerializerMethodField()
    identities = serializers.SerializerMethodField()

    class Meta:
        model = Registry
        fields = (
            'version',
            'latestRevision',
            'registryIdentity',
            'identities',
        )

    def get_version(self, obj):
        return {
            'major': obj.major,
            'minor': obj.minor,
            'patch': obj.patch
        }

    def get_latestRevision(self, obj):
        return obj.latest_revision

    def get_registryIdentity(self, obj):
        return {
            'name': obj.name,
            'description': obj.description,
            'time': {
                'begin': obj.date_created
            }
        }

    def get_identities(self, obj):
        tokens = obj.tokens.all()
        identities = {}

        for token in tokens:
            t = RegistryIdentitySerializer(token).data
            del t['id']
            identities[t['token']['category']] = [t]

        return identities
