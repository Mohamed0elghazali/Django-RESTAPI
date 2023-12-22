"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from tickets import views

router = DefaultRouter()
router.register('guest', views.viewsets_guest)
router.register('movie', views.viewsets_movie)
router.register('reservation', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    ## 1- without rest framework and no model query (FBV)
    path('django/jsonresponsenomodel/', views.no_rest_no_model),

    ## 2- without rest framework and with model query (FBV)
    path('django/jsonresponsewithmodel/', views.no_rest_with_model),

    ## 3- with rest framework and with model query (FBV) @api_view
    ## 3.1 GET - POST
    path('rest/fbvlist/', views.FBV_List),

    ## 3.2 GET - PUT - DELETE
    path('rest/fbvlist/<int:pk>', views.FBV_pk),

    ## 4- with rest framework and with model query (CBV) APIView
    ## 4.1 GET - POST
    path('rest/cbvlist/', views.CBV_List.as_view()),

    ## 4.2 GET - PUT - DELETE
    path('rest/cbvlist/<int:pk>', views.CBV_pk.as_view()),

    ## 5. with rest framework and with model query (CBV) using Mixins and Generics
    # 5.1 GET - POST
    path('rest/mixins_list/', views.mixins_list.as_view()),

    # 5.2 GET - PUI - DELETE
    path('rest/mixins_list/<int:pk>', views.mixins_pk.as_view()),

    ## 6. with rest framework and model query (CBV) using Generics 
    # 6.1 GET - POST
    path('rest/gererics_list/', views.generics_list.as_view()),

    # 6.2 GET - PUT - DELETE
    path('rest/gererics_list/<int:pk>', views.generics_pk.as_view()),

    ## 7. ViewSets
    path('rest/viewsets/', include(router.urls)),

    ## 8. Find a Movie using (FBV)
    path('django/find_movie/', views.find_moive),

    ## 9. Create a Reservation using (FBV)
    path('django/create_reservation/', views.create_reservation),

    ## 10. rest auth url ---> add option to login and logout.
    path('api-auth', include('rest_framework.urls')),

    ## 11. Token authentication
    path('api-token-auth', obtain_auth_token),

    ## 12. Post Author using generics
    path('post/generics/<int:pk>', views.Post_pk.as_view())

]

