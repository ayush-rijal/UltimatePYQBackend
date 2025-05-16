
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notification/', include('notification.urls')), # this is the url for notification api
    path('quizapi/',include('quizAPI.urls')), # this is the url for quiz api and result api
    path('userapi/', include('djoser.urls')),
    path("chatapi/", include("chat.urls", namespace="chat")),
    # path('userapi/',include('djoser.urls.jwt')),

    #since we are using custom jwt now so we need users url but for simple jwt we dont need this we need djoser.urls.jwt

    # path('blogapi/', include('blog.urls')),
    path('userapi/',include('users.urls')),
    path('todoapi/', include('todoList.urls')),
]

