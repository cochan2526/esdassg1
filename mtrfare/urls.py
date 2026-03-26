from django.urls import path
from . import views

urlpatterns = [
        path ( "" , views.homepage , name = "homepage" ) ,
        path ( "register/", views.register , name = "register" ) ,
        path ( "registering/", views.registering , name = "registering" ) ,
        path ( "logon/", views.logon , name = "logon" ) ,
        path ( "logging_on/", views.logging_on , name ="logging_on" ) ,
        path ( "logoff/" , views.logoff , name = "logoff" ) ,
        path ( "showfare/" , views.showfare , name = "showfare" ) ,
        path ( "barrfac/<int:station_id>/" , views.barrfac , name = "barrfac" ) ,
    ]

