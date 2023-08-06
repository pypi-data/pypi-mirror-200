from django.http import JsonResponse
from django.conf import settings

from rest_framework import status

from user_agents import parse


class UserAgentMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def _get_error(self):
        return JsonResponse(
            {"error": "Forbidden"},
            status=status.HTTP_403_FORBIDDEN
        )

    def __call__(self, request):
        ua_string = request.META.get('HTTP_USER_AGENT', None)
        tonic_ua_string = request.META.get('HTTP_TONIC_UA', None)

        if not any(path in request.path for path in settings.EXCLUDE_UA_PATHS):
            if ua_string is None and tonic_ua_string is None:
                return self._get_error()

            try:
                if settings.TONIC_AGENT not in ua_string:
                    return self._get_error()
            except (TypeError, AttributeError):
                pass

            try:
                if settings.TONIC_AGENT not in tonic_ua_string:
                    return self._get_error()
            except (TypeError, AttributeError):
                pass

        if ua_string:
            request.user_agent = parse(ua_string)
        else:
            request.user_agent = None

        return self.get_response(request)
