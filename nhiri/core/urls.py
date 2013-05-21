from django.conf.urls import patterns, url

from nhiri.core import views
from nhiri.core.views import twitter
from nhiri.core.views import api


urlpatterns = patterns(
    '',
    url(r'^twitter/auth', twitter.AuthView.as_view()),
    url(r'^twitter/fetch', twitter.FetchView.as_view()),
    url(r'^gps/fetch', views.GPSLoggerFetchView.as_view()),

    # API URLs
    url(r'api/moments', api.MomentList.as_view()),
    url(r'api/caffeine', api.CaffeineList.as_view())
)
