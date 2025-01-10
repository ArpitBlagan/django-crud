# middleware.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import User

class UserAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get("Token")

        if token:
            try:
                # Decode the token (replace with your actual secret key)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = User.objects.get(id=payload["user_id"])
                request.user = user  # Attach user to the request
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                return JsonResponse({"error": "Invalid or expired token"}, status=401)

        response = self.get_response(request)
        return response

# decorators.py
# from functools import wraps
# from django.http import JsonResponse
# import jwt
# from django.conf import settings
# from .models import User

# def jwt_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         token = request.COOKIES.get("Token")

#         if token:
#             try:
#                 # Decode the token (replace with your actual secret key)
#                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#                 user = User.objects.get(id=payload["user_id"])
#                 request.user = user  # Attach user to the request
#             except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
#                 return JsonResponse({"error": "Invalid or expired token"}, status=401)
#         else:
#             return JsonResponse({"error": "Authentication required"}, status=401)

#         return view_func(request, *args, **kwargs)

#     return _wrapped_view
