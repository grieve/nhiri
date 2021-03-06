from django.db import models


class Account(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    refreshed = models.DateTimeField(auto_now=True)


class TwitterAccount(Account):
    username = models.CharField(max_length=32)
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    tweet_count = models.PositiveIntegerField(default=0)
    access_token_key = models.TextField(default="")
    access_token_secret = models.TextField(default="")


class Moment(models.Model):
    when = models.DateTimeField()
    kind = models.CharField(max_length=10, default="text")
    account = models.ForeignKey(Account, null=True, editable=False)


class TwitterMoment(Moment):
    tweet_id = models.CharField(max_length=64)
    author = models.CharField(max_length=32)
    content = models.CharField(max_length=200)
    retweet = models.BooleanField(default=False)
    original_author = models.CharField(max_length=32, null=True)


class GPSMoment(Moment):
    latitude = models.FloatField()
    longitude = models.FloatField()


class CaffeineMoment(Moment):
    item = models.CharField(max_length=255)
    milligrams = models.PositiveIntegerField(default=0)
