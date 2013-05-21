from django.conf.urls import patterns, url
from nhiri.core.views import twitter


urlpatterns = patterns(
    '',
    url(r'^twitter/auth', twitter.AuthView.as_view()),
    url(r'^twitter/fetch', twitter.FetchView.as_view())
)
