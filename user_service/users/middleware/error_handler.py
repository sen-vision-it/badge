import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return JsonResponse({
                "type": "about:blank",
                "title": "Permission refusée",
                "status": 403,
                "detail": str(exception)
            }, status=403, content_type="application/problem+json")

        elif isinstance(exception, Http404):
            return JsonResponse({
                "type": "about:blank",
                "title": "Non trouvé",
                "status": 404,
                "detail": str(exception)
            }, status=404, content_type="application/problem+json")

        elif isinstance(exception, ValidationError):
            return JsonResponse({
                "type": "about:blank",
                "title": "Erreur de validation",
                "status": 400,
                "detail": exception.detail
            }, status=400, content_type="application/problem+json")

        elif isinstance(exception, (InvalidToken, TokenError)):
            return JsonResponse({
                "type": "about:blank",
                "title": "Échec de l'authentification",
                "status": 401,
                "detail": str(exception)
            }, status=401, content_type="application/problem+json")

        else:
            logger.error("Unhandled exception", exc_info=exception)
            return JsonResponse({
                "type": "about:blank",
                "title": "Erreur interne du serveur",
                "status": 500,
                "detail": "Une erreur inattendue s'est produite."
            }, status=500, content_type="application/problem+json")
