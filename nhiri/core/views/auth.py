from django.template.response import TemplateResponse
from django.views.generic.base import View


class TwitterAuthView(View):

    def get(self, request):

        return TemplateResponse(request, 'nhiri/core/auth/twitter.html')
