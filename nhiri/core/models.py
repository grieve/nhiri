from django.db import models


class Account(models.Model):
    class Meta:
        name = "Default"
        source = "Default"
        datatype = "text"
        mapping = {}

    created = models.DateTimeField()
    refreshed = models.DateTimeField()


class TwitterAccount(Account):
    class Meta:
        name = "Twitter"
        source = "http://twitter.com"
        datatype = "json"
        mapping = {

        }

    username = models.CharField(max_length=32)
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    tweet_count = models.PositiveIntegerField(default=0)


class Moment(models.Model):
    when = models.DateTimeField()
    kind = models.CharField(max_length=10, default="text")
    account = models.ForeignKey(Account)


class TwitterMoment(Moment):
    author = models.CharField(max_length=32)
    content = models.CharField(max_length=200)
    retweet = models.BooleanField(default=False)
    original_author = models.CharField(max_length=32, null=True)
