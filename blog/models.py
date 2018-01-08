from django.db import models
from django.utils import timezone

class Post(models.Model):
    mob_leader = models.CharField()
    mob1_spd = models.CharField()
    mob1_multi = models.CharField()
    mob2_spd = models.CharField()
    mob2_multi = models.CharField()
    mob3_spd = models.CharField()
    mob3_multi = models.CharField()
    mob4_spd = models.CharField()
    mob4_multi = models.CharField()
    #created_date = models.DateTimeField(
    #        default=timezone.now)
    #published_date = models.DateTimeField(
    #        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
