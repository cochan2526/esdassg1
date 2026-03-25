from django.db import models

# Create your models here.

#
#    Class Barrier Free Facility Category
#
# ﻿"Item_Code","Category_Id","Category_En","Category_Zh","Facility_En","Facility_Zh","Sorting_Order"
class BarrCat ( models.Model ) :
    Item_Code = models.CharField( max_length = 10 , unique = True )
    Category_Id = models.CharField ( max_length = 10 )
    Category_En = models.TextField ( )
    Category_Zh = models.TextField ( )
    Facility_En = models.TextField ( )
    Facility_Zh = models.TextField ( )
    Sorting_Order = models.IntegerField ( )

#
#    Class MTR Lines And Stations
#
# Line Code,Direction,Station Code,Station ID,Chinese Name,English Name,Sequence
class Station ( models.Model ) :
    Line_Code = models.CharField ( max_length = 3 )
    Direction = models.CharField ( max_length = 10 )
    Station_Code = models.CharField ( max_length = 3 )
    Station_ID = models.IntegerField ( unique = True )
    Chinese_Name = models.TextField ( )
    English_Name = models.TextField ( )
    Sequence = models.IntegerField ( )

#
#    Class Barrier Free Facility
#
# "Station_No","Key","Value","AJTextEn","AJTextZh","Exit_Coordinate_X_Y"
class BarrFac ( models.Model ) :
    Station = models.ForeignKey (
          Station , on_delete = models.CASCADE, related_name = "Inside"
          )
    BarrCat = models.ForeignKey (
          BarrCat , on_delete = models.CASCADE, related_name = "Is_kind_of"
          )
    Value = models.BooleanField ( )
    AJTextEn = models.TextField ( blank = True )
    AJTextZh = models.TextField ( blank = True )
    Exit_Coordinate_X_Y = models.TextField ( blank = True )

#
#    Class MTR Lines Fares
#
#    For the simplicity of this project, this table is NOT normalized
#
#    For a cleaner normalized implementation, the 2 stations column should
#    be removed and a journey table with journey ID and station ID as combine
#    key should be created and this table should point to the journey table
#    to avoid many to many relationship
#
# SRC_STATION_NAME,SRC_STATION_ID,DEST_STATION_NAME,DEST_STATION_ID,OCT_ADT_FARE,OCT_STD_FARE,OCT_JOYYOU_SIXTY_FARE,SINGLE_ADT_FARE,OCT_CON_CHILD_FARE,OCT_CON_ELDERLY_FARE,OCT_CON_PWD_FARE,SINGLE_CON_CHILD_FARE,SINGLE_CON_ELDERLY_FARE
class Fare ( models.Model ) :
    Source_Station = models.ForeignKey (
          Station , on_delete = models.CASCADE, related_name = "Departing_From"
          )
    Destination_Station = models.ForeignKey (
          Station , on_delete = models.CASCADE, related_name = "Destination"
          )
    Octopus_Card_Adult = models.DecimalField(max_digits=6, decimal_places=2)
    Octopus_Card_Student = models.DecimalField(max_digits=6, decimal_places=2)
    Octopus_Card_60 = models.DecimalField(max_digits=6, decimal_places=2)
    Single_Ticket = models.DecimalField(max_digits=6, decimal_places=2)
    Octopus_Card_Children = models.DecimalField(max_digits=6, decimal_places=2)
    Octopus_Card_Elderly = models.DecimalField(max_digits=6, decimal_places=2)
    Octopus_Card_Disabled = models.DecimalField(max_digits=6, decimal_places=2)
    Single_Ticket_Children = models.DecimalField(max_digits=6, decimal_places=2)
    Single_Ticket_Elderly = models.DecimalField(max_digits=6, decimal_places=2)

