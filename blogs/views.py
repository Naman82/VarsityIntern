from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from blogBackend.utils import send_response
from django.utils.decorators import method_decorator
from .models import *
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_social_oauth2.authentication import SocialAuthentication
from .serializers import BlogSerializer,CommentSerializer
from django.http import JsonResponse
from django.db.models import Q

from django.shortcuts import get_object_or_404
class BlogView(APIView):
    authentication_classes = [OAuth2Authentication,SocialAuthentication]
    def get(self,request):
        try:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs,many=True)
            return JsonResponse(serializer.data,safe=False)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description='Title of blog'),
                "meta_title": openapi.Schema(type=openapi.TYPE_STRING,description="meta title of blog"),
                "body": openapi.Schema(type=openapi.TYPE_STRING,description="body of blog"),
                "tags": openapi.Schema(type=openapi.TYPE_STRING,description="tags of blog"),
                # "image": openapi.Schema(type=openapi.TYPE_STRING, description="image URL of the blog"),
            }
        ),
        responses={
            200: "ok",
            400: "not valid",
        }
    )
    def post(self,request,format=None):
        try:
            user = request.user
            title = request.data['title']
            meta_title = request.data['meta_title']
            body = request.data['body']
            tags = request.data['tags']
            
            blog = Blog(user=user,title=title,meta_title=meta_title,body=body,tags=tags)
            blog.save()
            return send_response(result=True,message="Blog created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class BlogViewDetail(APIView):
    authentication_classes = [OAuth2Authentication,SocialAuthentication]
    def get(self,request,pk,format=None):
        try:
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog)
            return send_response(result=True,data=serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description='Title of blog'),
                "meta_title": openapi.Schema(type=openapi.TYPE_STRING,description="meta title of blog"),
                "body": openapi.Schema(type=openapi.TYPE_STRING,description="body of blog"),
                "tags": openapi.Schema(type=openapi.TYPE_STRING,description="tags of blog"),
                # "image": openapi.Schema(type=openapi.TYPE_STRING, description="image URL of the blog"),
            }
        ),
        responses={
            200: "ok",
            400: "not valid",
        }
    )
    def patch(self,request,pk,format=None):
        try:
            blog = Blog.objects.get(pk=pk)

            if request.user != blog.user:
                return send_response(result=False,message="You do not have permission to update this blog")

            if 'title' in request.data:
                blog.title = request.data['title']
            if 'meta_title' in request.data:
                blog.meta_title = request.data['meta_title']
            if 'body' in request.data:
                blog.body = request.data['body']
            if 'tags' in request.data:
                blog.tags = request.data['tags']
            blog.save()
            return send_response(result=True,message="Blog updated successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    def delete(self,request,pk,format=None):
        try:
            blog = Blog.objects.get(pk=pk)
            blog.delete()
            return send_response(result=True,message="Blog successfully deleted")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

# COMMENT CODE

class CommentViewDetail(APIView):
    authentication_classes = [OAuth2Authentication,SocialAuthentication]

    def get(self,request,pk):
        try:
            blog = Blog.objects.get(pk=pk)
            comments = Comment.objects.filter(blog=blog)
            serializer = CommentSerializer(comments,many=True)
            return JsonResponse(serializer.data,safe=False)
        except Exception as e:
            return send_response(result=False, message=str(e))
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "blog": openapi.Schema(type=openapi.TYPE_INTEGER, description='Id of blog'),
                "parent": openapi.Schema(type=openapi.TYPE_INTEGER,description="null if not reply otherwise Id of comment"),
                "text": openapi.Schema(type=openapi.TYPE_STRING,description="comment content"),
            }
        ),
        responses={
            200: "ok",
            400: "not valid",
        }
    )    
    def post(self,request,pk):
        try:
           blog = Blog.objects.get(pk=pk)
           parent = request.data['parent']
           comment = Comment(user=request.user,blog=blog,parent=parent,text=request.data['text'])
           comment.save()
           return send_response(result=True,message="comment created successfully") 
        except Exception as e:
            return send_response(result=False, message=str(e))

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(type=openapi.TYPE_STRING,description="comment content"),
            }
        ),
        responses={
            200: "ok",
            400: "not valid",
        }
    )     
    def patch(self,request,pk):
        try:
            comment = Comment.objects.get(pk=pk)
            if 'text' in request.data:
                comment.text = request.data['text']
                comment.save()
            return send_response(result=True,message="comment edited successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    def delete(self,request,pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return send_response(result=True,message="Comment deleted successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

# Search Functionality

class SearchView(APIView):
    def get(self,request):
        try:
            query = request.query_params.get('query', '')
            results = Blog.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
            serializer = BlogSerializer(results, many=True)
            return send_response(result=True,data=serializer.data)
        except Exception as e:
            return send_response(result=False, message=str(e))  