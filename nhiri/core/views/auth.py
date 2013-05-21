from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

from nhiri.core import models

import tweepy
import logging


class TwitterAuthView(View):

    def get(self, request):
        auth = tweepy.OAuthHandler(
            settings.API_KEYS['twitter']['key'],
            settings.API_KEYS['twitter']['secret'],
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
