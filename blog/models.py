from django.db import models
from django.utils import timezone


class Post(models.Model):

    ip = models.CharField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_data = timezone.now()
        self.save()

    def __str__(self):
        return "IPYShow"


class IpyTest(models.Model):

    A = 'A'
    B = 'B'
    C = 'C'
    class_choices = ((A, 'Class A'),
                     (B, 'Class B'),
                     (C, 'Class C'))
    ip = models.CharField("IP", max_length=35)
    binary_ip = models.CharField(max_length=35)
    binary_mask = models.CharField(max_length=35)
    cidr_mask = models.CharField(max_length=15)
    network_ip = models.CharField(max_length=15)
    broadcast_ip = models.CharField(max_length=15)
    class_ip = models.CharField(max_length=3, choices=class_choices)

    def __str__(self):
        return "IPYTest"
