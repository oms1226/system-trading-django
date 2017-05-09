from django.db import models
from django.utils.timezone import now


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    use_yn = models.CharField(max_length=1, default='Y')
    desc = models.TextField(blank=True)

    class Meta:
        abstract = True


class StockCode(BaseModel):
    yahoo_code = models.CharField(db_index=True, max_length=200)
    name = models.CharField(max_length=500)


class StrategyBuy(BaseModel):
    code = models.CharField(db_index=True, max_length=200)
    name = models.CharField(max_length=500)


class StrategySell(BaseModel):
    code = models.CharField(db_index=True, max_length=200)
    name = models.CharField(max_length=500)


class StockData(BaseModel):
    code = models.CharField(db_index=True, max_length=200)
    date = models.CharField(db_index=True, max_length=10)
    open = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    close = models.FloatField(null=True)
    adj_close = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    ma_5 = models.FloatField(null=True)
    ma_20 = models.FloatField(null=True)
    ma_60 = models.FloatField(null=True)
    mv_5 = models.FloatField(null=True)
    mv_20 = models.FloatField(null=True)
    mv_60 = models.FloatField(null=True)
    ra_5 = models.FloatField(null=True)
    ra_20 = models.FloatField(null=True)

    class Meta:
        unique_together = ('code', 'date')





