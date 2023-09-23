from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication
from rest_framework.parsers import FormParser,MultiPartParser
from social_django.models import UserSocialAuth
from blogBackend.utils import send_response
from drf_social_oauth2.views import TokenView, ConvertTokenView

from .models import *
from .serializers import *


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="Save User Details",
    tags=["User Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password':openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        }
    )
))
class UserView(APIView):

    def post(self, request):
        try:
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            if email is not None and password is not None:
                user = User.objects.filter(email=email)
                if not user.exists():
                    new_user=User.objects.create_user(email=email, password=password)
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


#PROFILE SECTION

class ProfileView(APIView):
    authentication_classes = [OAuth2Authentication,SocialAuthentication]
    parser_classes = [FormParser,MultiPartParser]
    def get(self,request):
        try:
            userProfile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(userProfile)
            return send_response(result=True,data=serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "name": openapi.Schema(type=openapi.TYPE_STRING, description='name'),
    #             "bio": openapi.Schema(type=openapi.TYPE_STRING,description="bio"),
    #             "profile_pic": openapi.Schema(type=openapi.TYPE_STRING, description="image URL of the user"),
    #         }
    #     ),
    #     responses={
    #         200: "ok",
    #         400: "not valid",
    #     }
    # )    
    def patch(self,request):
        try:
            userProfile = UserProfile.objects.get(user=request.user)
            if 'name' in request.data:
                userProfile.name = request.data['name']
            if 'bio' in request.data:
                userProfile.bio = request.data['bio']
            if 'profile_pic' in request.data:
                userProfile.profile_pic= request.data['profile_pic']
            userProfile.save()
            return send_response(result=True,message="User Profile Updated")
        except Exception as e:
            return send_response(result=False, message=str(e))
        