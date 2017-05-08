from django.contrib import admin
from .models import StockCode, StrategyBuy, StrategySell, StockData

# Register your models here.


class StockCodeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StockCode._meta.fields]

admin.site.register(StockCode, StockCodeAdmin)


class StrategyBuyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StrategyBuy._meta.fields]

admin.site.register(StrategyBuy, StrategyBuyAdmin)


class StrategySellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StrategySell._meta.fields]

admin.site.register(StrategySell, StrategySellAdmin)


class StockDataAdmin(admin.ModelAdmin):
    list_display = [f.name for f in StockData._meta.fields]

admin.site.register(StockData, StockDataAdmin)


