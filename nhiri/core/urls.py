from django.conf.urls import patterns, url
from nhiri.core.views.auth import TwitterAuthView


urlpatterns = patterns(
    '',
    url(r'^auth/twitter', TwitterAuthView.as_view())
)
