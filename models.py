from django.db import models
from django.utils import timezone

# Create your models here.


class Recipient(models.Model):
    email = models.EmailField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Information(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.title)

    @staticmethod
    def get_or_default(name, default_title, default_text):
        try:
            information = Information.objects.get(pk=name)
        except Information.DoesNotExist:
            information = Information(name=name, title=default_title, text=default_text)
            information.save()

        return information


class Email(models.Model):
    company = models.CharField(max_length=32, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    telephone = models.CharField(max_length=32, blank=True)
    message = models.TextField()
    privacy_accepted = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    received_on = models.DateTimeField(default=timezone.now)
