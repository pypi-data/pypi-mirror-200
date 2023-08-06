import logging

logger = logging.getLogger()


class ProfessionIdMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_profession_id = request.META.get('HTTP_PROFESSION_ID', None)

        profession_id = None
        try:
            profession_id = int(user_profession_id)
        except ValueError as e:
            logger.warning('The profession id of the user is not a int number.' +
                           f'User profession id: {user_profession_id}; {e}')
        except TypeError:
            pass

        request.profession_id = profession_id
        response = self.get_response(request)

        return response
