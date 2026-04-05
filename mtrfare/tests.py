from django.test import Client , TestCase
from django.contrib.auth.models import User
from .models import BarrFac , Station , BarrCat , UserPref , Fare

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
#
# Test if facility is displayed
#
    def test_barrfac_page_displayed ( self ) :
        client = Client ( )
        response = self.client.get ( "/barrfac/1/" )
        self.assertContains ( response , "Barrier free facilities in the Central station" )
        self.assertContains ( response , "Accessible Toilets (Paid Area)" )

class UserRegTest ( TestCase ) :
    @classmethod
    def setUpTestData ( cls ) :
        cls.userT1 = User.objects.create_user ( username = "userT1" , password = "pwdT1" )
        cls.userpref = UserPref.objects.create (
            User = cls.userT1 ,
            Pref_source_station_id = 1 ,
            Pref_dest_station_id = 3 ,
            Pref_barrier_free_facilities = json.dumps ( { "Category" : [ "MJ" , "VJ" ] , "Facility" : [ "HJ7" , "AJ9" ] } )
            )

    def test_usert1 ( self ) :
        self.assertEqual ( self.userT1.username , "userT1" )

# view test
#
# Test if "Guest" is displayed if not logged on
#
    def test_hongpage ( self ) :
        client = Client ( )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello Guest !" )

#
# Test if username is displayed if logged on
#
    def test_logon ( self ) :
        client = Client ( )
        response = self.client.force_login ( self.userT1 )
        response = self.client.get ( "" )
        self.assertContains ( response , "Hello userT1 !" )

#
# test logon through logon page
#
# follow redirect to avoid test fail for 302 error
# https://stackoverflow.com/questions/17352314/django-test-client-post-returns-302-despite-error-on-views-post
#
    def test_logginon ( self ) :
        client = Client ( )
        response = self.client.post ( "/logging_on/" , { "username" : "userT1" , "password" : "pwdT1" } , follow = True )
        self.assertContains ( response , "Hello userT1 !" )

class ShowFareTest ( TestCase ) :
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
        cls.station3 = Station.objects.create (
            Line_Code = "TWL" ,
            Direction = "DT" ,
            Station_Code = "TST" ,
            Station_ID = 3 ,
            Chinese_Name = "尖沙咀" ,
            English_Name = "Tsim Sha Tsui" ,
            Sequence = 14
            )
        cls.barrcat3 = BarrCat.objects.create (
            Item_Code = "MJ4" ,
            Category_Id = "MJ" ,
            Category_En = "Facilities for Mobility Impaired" ,
            Category_Zh = "行動不便人士設施" ,
            Facility_En = "Accessible Toilets (Unpaid Area)" ,
            Facility_Zh = "無障礙洗手間 (閘外區域)" ,
            Sorting_Order = 6 ,
            )
        cls.barrfac3 = BarrFac.objects.create (
            Station = cls.station3 ,
            BarrCat = cls.barrcat3 ,
            Value = True ,
            AJTextEn = "" ,
            AJTextZh = "" ,
            Exit_Coordinate_X_Y = "" ,
            )
        cls.userT1 = User.objects.create_user ( username = "userT1" , password = "pwdT1" )
        cls.userpref = UserPref.objects.create (
            User = cls.userT1 ,
            Pref_source_station_id = 1 ,
            Pref_dest_station_id = 3 ,
            Pref_barrier_free_facilities = json.dumps ( { "Category" : [ "MJ" , "VJ" ] , "Facility" : [ "HJ7" , "AJ9" ] } )
            )
        cls.fare = Fare.objects.create (
            Source_Station = cls.station ,
            Destination_Station = cls.station3,
            Octopus_Card_Adult = 10.6 ,
            Octopus_Card_Student = 5.4 ,
            Octopus_Card_60 = 2.1 ,
            Single_Ticket = 12.5 ,
            Octopus_Card_Children = 5.4 ,
            Octopus_Card_Elderly = 2.1 ,
            Octopus_Card_Disabled = 2.1 ,
            Single_Ticket_Children = 5.5 ,
            Single_Ticket_Elderly = 5.5 ,
            )

# view test

#
# first test to ensure the barrier free facilities is there and displayed.
#
    def test_barrfac_page_displayed ( self ) :
        client = Client ( )
        response = self.client.get ( "/barrfac/1/" )
        self.assertContains ( response , "Barrier free facilities in the Central station" )
        self.assertContains ( response , "Accessible Toilets (Paid Area)" )

    def test_barrfac_page_displayed ( self ) :
        client = Client ( )
        response = self.client.get ( "/barrfac/3/" )
        self.assertContains ( response , "Barrier free facilities in the Tsim Sha Tsui station" )
        self.assertContains ( response , "Accessible Toilets (Unpaid Area)" )

#
# test if facilities in user preference will be shown
# together with fare when logged on
#
    def test_showfare ( self ) :
        client = Client ( )
        response = self.client.force_login ( self.userT1 )
        response = self.client.post ( "/showfare/" , { "Departing From" : "1" , "Going To" : "3" } )
        self.assertContains ( response , "Hello userT1 !" )
        self.assertContains ( response , "Octopus Card Adult : 10.60" )
        self.assertContains ( response , "Single Ticket : 12.50" )
        self.assertContains ( response , "Barrier Free Facilities in concern in Central Station" )
        self.assertContains ( response , "Accessible Toilets (Paid Area)" )
        self.assertContains ( response , "Barrier Free Facilities in concern in Tsim Sha Tsui Station" )
        self.assertContains ( response , "Accessible Toilets (Unpaid Area)" )

