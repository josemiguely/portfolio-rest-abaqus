from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: add deleted_at if neccesary later
    
    class Meta:
        abstract = True

class Asset(TimeStampModel):
    name = models.CharField(max_length=200, unique=True)

class Price(TimeStampModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    #TODO: Later find out highest price and most decimal values and get from that max_digits
    value = models.DecimalField(max_digits=20, decimal_places=10)

class Portfolio(TimeStampModel):
   name = models.CharField(max_length=200, unique=True)
   initial_value = models.DecimalField(max_digits=20, decimal_places=10, default=1_000_000_000)

class Quantity(TimeStampModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=10)

class Weight(TimeStampModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=6)

