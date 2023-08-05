from django.utils import timezone
from django.db import models

import uuid


class AuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name_plural = 'Auth Tokens'
    

class Token(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        BURNED = 'burned'

    category = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, default='')
    symbol = models.CharField(max_length=100)
    decimals = models.PositiveIntegerField(default=0)
    icon = models.ImageField(null=True, blank=True)
    is_nft = models.BooleanField(default=False)
    nft_description = models.CharField(max_length=255, default='')
    nft_types = models.JSONField(default=dict)
    '''
        NFT_TYPES
        {
            "commitment_string_here": {
                "name": "NFT #0",
                "description": "",
                "fields": [],
                "uris": {
                    "icon": "https://gist.githubusercontent.com/mr-zwets/0e698a88323465686437b5e70a8ccf56/raw/Eo_circle_blue_number-0.svg"
                }
            }
        }
    '''
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    owner = models.ForeignKey(
        AuthToken,
        related_name='tokens',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    class Meta:
        ordering = (
            'name',
            'symbol',
            'is_nft',
        )


class Registry(models.Model):
    major = models.PositiveIntegerField(default=0) # incremented when an identity is removed
    minor = models.PositiveIntegerField(default=0) # incremented when an identity is added
    patch = models.PositiveIntegerField(default=0) # incremented when an identity is modified
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    latest_revision = models.DateTimeField(default=timezone.now)
    tokens = models.ManyToManyField(Token)
    # owner = models.ForeignKey(
    #     AuthToken,
    #     related_name='registries',
    #     on_delete=models.PROTECT,
    #     null=True,
    #     blank=True
    # )

    class Meta:
        verbose_name_plural = 'Registries'
        ordering = ('name', )

    def save(self, *args, **kwargs):
        self.latest_revision = timezone.now()
        super(Registry, self).save(*args, **kwargs)
