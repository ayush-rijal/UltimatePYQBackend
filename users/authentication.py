
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
                print("🔍 Cookie Token:", raw_token)  # Debug log
            else:
                raw_token = self.get_raw_token(header)
                print("🔍 Header Token:", raw_token)  # Debug log

            if raw_token is None:
                print("❌ No Token Found")
                return None

            validated_token = self.get_validated_token(raw_token)
            print("✅ Token Validated:", validated_token)

            user = self.get_user(validated_token)
            print("👤 Authenticated User:", user)

            return user, validated_token
        except Exception as e:
            print("❌ Authentication Error:", str(e))
            return None
