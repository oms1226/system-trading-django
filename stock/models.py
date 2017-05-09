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
    type = models.CharField(db_index=True, max_length=100, default="DEFAULT")
    yahoo = models.CharField(db_index=True, max_length=200)
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
    open = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    close = models.FloatField(default=0)
    adj_close = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    ma_5 = models.FloatField(default=0)
    ma_20 = models.FloatField(default=0)
    ma_60 = models.FloatField(default=0)
    mv_5 = models.FloatField(default=0)
    mv_20 = models.FloatField(default=0)
    mv_60 = models.FloatField(default=0)
    ra_5 = models.FloatField(default=0)
    ra_20 = models.FloatField(default=0)

    class Meta:
        unique_together = ('code', 'date')








