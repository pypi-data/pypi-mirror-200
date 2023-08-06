from django.contrib import admin

from bcmr.models import *


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = [
        'id',
    ]

class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'is_nft',
        'category',
        'name',
        'symbol',
        'decimals',
        'status',
        'date_created',
    ]

class RegistryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'active',
        'description',
        'date_created',
        'latest_revision',
    ]


admin.site.register(AuthToken, AuthTokenAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Registry, RegistryAdmin)
