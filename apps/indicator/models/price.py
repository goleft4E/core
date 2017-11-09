from datetime import timedelta

from django.db import models
from unixtimestampfield.fields import UnixTimeStampField

from apps.channel.models.exchange_data import SOURCE_CHOICES


class Price(models.Model):
    source = models.SmallIntegerField(choices=SOURCE_CHOICES, null=False)
    coin = models.CharField(max_length=6, null=False, blank=False)

    price_satoshis = models.BigIntegerField(null=False) # price_satoshis
    price_wei = models.BigIntegerField(null=True)  # wei
    price_usdt = models.FloatField(null=True) # USD value

    timestamp = UnixTimeStampField(null=False)


    # MODEL PROPERTIES

    # MODEL FUNCTIONS

    @property
    def price_satoshis_change(self):

        past_price = Price.objects.filter(
            source=self.source,
            coin=self.coin,
            timestamp__lte=self.timestamp - timedelta(minutes=15)
        ).order_by("-timestamp").first()

        if past_price:
            return float(self.price_satoshis - past_price.price_satoshis) / past_price.price_satoshis

    def price_usdt_change(self):
        btc_price = Price.objects.filter(
            source=self.source,
            coin=self.coin,
            timestamp__gte=self.timestamp - timedelta(minutes=1),
            timestamp__lte=self.timestamp + timedelta(minutes=1),
            price_usdt__isnull=False
        ).first()
        if btc_price:
            return btc_price.price_usdt
