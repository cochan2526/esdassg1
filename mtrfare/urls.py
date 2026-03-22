from django.urls import path
from . import views

urlpatterns = [
        path ( "" , views.homepage , name = "homepage" ) ,
        path ( "register/", views.register , name ="register" ) ,
        path ( "registering/", views.registering , name ="registering" ) ,
#         path ( "logon/", views.register , name ="logon" ) ,
#         path ( "logging_on/", views.registering , name ="logging_on" ) ,
    ]

