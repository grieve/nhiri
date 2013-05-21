from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

from nhiri.core import models

import tweepy


class AuthView(View):

    def get(self, request):
        auth = tweepy.OAuthHandler(
            settings.SOURCE_CONF['twitter']['key'],
            settings.SOURCE_CONF['twitter']['secret'],
            "http://%s%s" % (request.get_host(), request.get_full_path())
        )
        if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
            request_token = request.session.get('twitter_request_token')
            auth.set_request_token(request_token[0], request_token[1])
            try:
                auth.get_access_token(request.GET['oauth_verifier'])
            except:
                return redirect("http://%s%s" % (request.get_host(), request.get_full_path().split('?')[0]))
            api = tweepy.API(auth)
            user = api.verify_credentials()
            account, created = models.TwitterAccount.objects.get_or_create(username=user.screen_name)
            account.access_token_key = auth.access_token.key
            account.access_token_secret = auth.access_token.secret
            account.followers = user.followers_count
            account.following = user.friends_count
            account.tweet_count = user.statuses_count
            account.save()
            if 'redirect_after_auth' in request.session:
                return redirect(request.session.pop('redirect_after_auth'))
            else:
                return redirect('/')
        else:
            auth_url = auth.get_authorization_url()
            request.session['twitter_request_token'] = (auth.request_token.key, auth.request_token.secret)
            if 'redirect' in request.GET:
                request.session['redirect_after_auth'] = request.GET['redirect']
            return redirect(auth_url)


class FetchView(View):

    def get(self, request):
        auth = tweepy.OAuthHandler(
            settings.SOURCE_CONF['twitter']['key'],
            settings.SOURCE_CONF['twitter']['secret'],
            "http://%s%s" % (request.get_host(), request.get_full_path())
        )
        for account in models.TwitterAccount.objects.all():
            auth.set_access_token(account.access_token_key, account.access_token_secret)
            api = tweepy.API(auth)
            timeline = api.user_timeline()
            new_tweets = []
            for status in timeline:
                tweet, new = models.TwitterMoment.objects.get_or_create(
                    tweet_id=status.id,
                    when=status.created_at
                )
                if not new:
                    continue
                tweet.account = account
                tweet.kind = "twitter"
                tweet.content = status.text
                tweet.author = status.author.screen_name
                if hasattr(status, 'retweeted_status'):
                    tweet.retweet = True
                    tweet.original_author = status.retweeted_status.author.screen_name
                    tweet.content = status.retweeted_status.text
                tweet.save()
                new_tweets.append(status.id)

            return HttpResponse('%d new tweets: %s' % (len(new_tweets), new_tweets))
