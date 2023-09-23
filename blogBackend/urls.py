from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


admin.site.site_header  =  "Admin Panel - VarsityBlog"  
admin.site.site_title  =  "Admin Panel - VarsityBlog"
admin.site.index_title  =  "VarsityBlog"

schema_view = get_schema_view(
    openapi.Info(
        title="VarsityBlog API",
        default_version='v1',
        description="VarsityBlog APIs "
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('users.urls')),
    path('api/',include('blogs.urls')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)