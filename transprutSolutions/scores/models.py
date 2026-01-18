from django.db import models


class ScoreEntry(models.Model):
    score = models.FloatField()
    time = models.FloatField()
    hp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
