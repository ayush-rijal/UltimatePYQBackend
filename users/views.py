from django.conf import settings
from rest_framework.views import APIView  ##for logout
from rest_framework.response import Response #for logout
from rest_framework import status #for status 
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)   ##these views are to be overriden

class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  ##overriding post only no the get

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                # max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                # max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response




class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs) 

        '''
        ✅ This calls the original post method from TokenObtainPairView, which does two things:
                Validates the user’s credentials.
                Generates the JWT tokens (access and refresh) and returns them in response.data.
        '''



        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                # max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                # domain=settings.BACKEND_DOMAIN,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                # max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                # domain=settings.BACKEND_DOMAIN,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh') ##instead of grabbing from bodies gradb it from cookies

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                # max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response




class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token  ##placing in request body

        return super().post(request, *args, **kwargs)
    

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    
# # More secure logout 
# class LogoutView(APIView):
#     def post(self, request, *args, **kwargs):
#         response = Response(status=status.HTTP_204_NO_CONTENT)

#         # Deleting the cookies with the correct path and domain as per the settings
#         response.delete_cookie('access', path=settings.AUTH_COOKIE_PATH, domain=settings.BACKEND_DOMAIN)
#         response.delete_cookie('refresh', path=settings.AUTH_COOKIE_PATH, domain=settings.BACKEND_DOMAIN)

#         return response    