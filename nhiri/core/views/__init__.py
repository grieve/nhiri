from django.views.generic.base import View
from django.http import HttpResponse
from django.conf import settings

from nhiri.core import models
import datetime
import requests
from requests.auth import HTTPBasicAuth
import logging


class GPSLoggerFetchView(View):
    def get(self, request):
        todays_url = settings.SOURCE_CONF['gps']['source'] + datetime.datetime.now().strftime("%Y%m%d") + ".txt"
        req_auth = HTTPBasicAuth(
            settings.SOURCE_CONF['gps']['username'],
            settings.SOURCE_CONF['gps']['password']
        )
        logging.error(todays_url)
        coords = requests.get(todays_url, auth=req_auth)
        rows = coords.text.split('\n')
        new_moments = []
        for row in rows:
            logging.error(row)
            values = row.split(',')
            if values[0] == "time" or values[0].startswith('1977'):
                continue
            moment, new = models.GPSMoment.objects.get_or_create(
                when=datetime.datetime.strptime(values[0], "%Y-%m-%dT%H:%M:%SZ"),
                latitude=float(values[1]),
                longitude=float(values[2]),
                kind="gps"
            )
            if new:
                new_moments.append(values[0])

        return HttpResponse("%d new moments: %s" % (len(new_moments), new_moments))
