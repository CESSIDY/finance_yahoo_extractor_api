from django.db import models


class Companies(models.Model):
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return self.symbol


class Analytics(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, blank=True)
    date = models.DateField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    adj = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.company}: {self.date}"
