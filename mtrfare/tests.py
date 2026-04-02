from django.test import Client , TestCase
from django.contrib.auth.models import User
from .models import BarrFac , Station , BarrCat , UserPref

import json

# Create your tests here.

class BarrFacTest ( TestCase ) :
    @classmethod
    def setUpTestData ( cls ) :
        cls.station = Station.objects.create (
            Line_Code = "TWL" ,
            Direction = "DT" ,
            Station_Code = "CEN" ,
            Station_ID = 1 ,
            Chinese_Name = "中環" ,
            English_Name = "Central" ,
            Sequence = 16
            )
        cls.barrcat = BarrCat.objects.create (
            Item_Code = "MJ5" ,
            Category_Id = "MJ" ,
            Category_En = "Facilities for Mobility Impaired" ,
            Category_Zh = "行動不便人士設施" ,
            Facility_En = "Accessible Toilets (Paid Area)" ,
            Facility_Zh = "無障礙洗手間 (已付車費區域)" ,
            Sorting_Order = 7 ,
            )
        cls.barrfac = BarrFac.objects.create (
            Station = cls.station ,
            BarrCat = cls.barrcat ,
            Value = True ,
            AJTextEn = "" ,
            AJTextZh = "" ,
            Exit_Coordinate_X_Y = "" ,
            )

# view test

    def test_barrfac_page_displayed ( self ) :
        client = Client ( )
        response = self.client.get ( "/barrfac/1/" )
        self.assertContains ( response , "Barrier free facilities in the station" )
        self.assertContains ( response , "Accessible Toilets (Paid Area)" )

class UserRegTest ( TestCase ) :
    @classmethod
    def setUpTestData ( cls ) :
        cls.user = User.objects.create_user ( username = "userT1" , password = "pwdT1" )
        cls.userpref = UserPref.objects.create (
            username = "userT1" ,
            pref_source_station_id = 1 ,
            pref_dest_station_id = 3 ,
            pref_barrier_free_facilities = json.dumps ( { "Category" : [ "MJ" , "VJ" ] , "Facility" : [ "HJ7" , "AJ9" ] } )
            )

    def test_usert1 ( self ) :
        self.assertEqual ( self.user.username , "userT1" )

# view test

    def test_hongpage ( self ) :
        client = Client ( )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello Guest !" )

    def test_logon ( self ) :
        client = Client ( )
        response = self.client.force_login ( self.user )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello userT1 !" )



