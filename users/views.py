from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication
from social_django.models import UserSocialAuth
from blogBackend.utils import send_response
# from .serializers import PatientProfileSerializer,ConsultantProfileSerializer
from drf_social_oauth2.views import TokenView, ConvertTokenView
from django.http import JsonResponse
image_id = openapi.Parameter('id', openapi.IN_QUERY, description="Id of object to delete", type=openapi.TYPE_INTEGER)
from .models import *


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Save User Details",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_type':openapi.Schema(type=openapi.TYPE_INTEGER,description="1 for Patient, 2 for Consultant"),
            'email':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        }
    )
))
class UserView(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        try:
            if email is not None and password is not None:
                user = User.object.filter(email=email)
                if not user.exists():
                    new_user=User.object.create_user(email=email, password=password)
                    new_user.save()
                    new_user_profile = UserProfile(user=new_user)
                    new_user_profile.save()
                    return send_response(result=True, message="User created successfully")
                else:
                    if UserSocialAuth(user=user[0]).user_exists():
                        return send_response(result=False, message="Please login using socials")
                    return send_response(result=False, message="User with this email already exists")
            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False, message=str(e))

# AUTHENTICATION EXTENDED VIEWS

@method_decorator(name="post", decorator=swagger_auto_schema(
     operation_description="Test for login",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'client_id': openapi.Schema(type=openapi.TYPE_STRING, description="Client Id (VarsityBlog)"),
            'client_secret': openapi.Schema(type=openapi.TYPE_STRING, description="Client Secret (VarsityBlog)"),
            'grant_type':openapi.Schema(type=openapi.TYPE_STRING, description="Should be 'password' ",),
            'username':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Username (Email)"),
            'password':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Password")
        }
    ),
))
class TokenViewNew(TokenView):
    pass

@method_decorator(name="post", decorator=swagger_auto_schema(
     operation_description="Test for login",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'client_id': openapi.Schema(type=openapi.TYPE_STRING, description="Client Id (Casa Arch)"),
            'client_secret': openapi.Schema(type=openapi.TYPE_STRING, description="Client Secret (Casa Arch)"),
            'grant_type':openapi.Schema(type=openapi.TYPE_STRING, description="Should be 'convert_token' ",),
            'backend':openapi.Schema(type=openapi.TYPE_STRING, description="'google-oauth2' for google"),
            'token':openapi.Schema(type=openapi.TYPE_STRING, description="token"),
        }
    ),
))
class convertTokenViewNew(ConvertTokenView):
    pass