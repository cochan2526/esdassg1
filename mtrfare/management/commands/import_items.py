import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from mtrfare.models import BarrCat , BarrFac , Station , Fare


from pprint import pprint


class Command(BaseCommand):
    help = "Import data from the offline CSV dataset."

    def import_barrcat ( self ) :
        csv_path = Path(__file__).resolve().parents[3] / "data" / "barrcat.csv"
        imported = 0
        updated = 0

#         with csv_path.open(newline="", encoding="utf-8") as csv_file:
        with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                barrcat , created = BarrCat.objects.update_or_create(
                    Item_Code = row [ "Item_Code" ] ,
                    defaults={
                        "Item_Code" : row[ "Item_Code" ] ,
                        "Category_Id" : row[ "Category_Id" ] ,
                        "Category_En" : row[ "Category_En" ] ,
                        "Category_Zh" : row[ "Category_Zh" ] ,
                        "Facility_En" : row[ "Facility_En" ] ,
                        "Facility_Zh" : row[ "Facility_Zh" ] ,
                        "Sorting_Order" : int ( row[ "Sorting_Order" ] ) ,
                    },
                )
                if created:
                    imported = imported + 1
                else:
                    updated = updated + 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {imported} created, {updated} updated."
            )
        )

    def import_barrfac ( self ) :
        csv_path = Path(__file__).resolve().parents[3] / "data" / "barrfac.csv"
        imported = 0
        updated = 0

#         with csv_path.open(newline="", encoding="utf-8") as csv_file:
        with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                #
                # Create the departing ( source )
                # and destination station instance
                #
                station = Station.objects.get ( Station_ID = row [ "Station_No" ] )
                facility_category = BarrCat.objects.get ( Item_Code = row [ "Key" ] )

                barrfac , created = BarrFac.objects.update_or_create(
                    Station = station ,
                    BarrCat = facility_category ,
                    defaults={
                        "Value" : ( row[ "Value" ]  == "Y" ) ,
                        "AJTextEn" : row[ "AJTextEn" ] ,
                        "AJTextZh" : row[ "AJTextZh" ] ,
                        "Exit_Coordinate_X_Y" : row[ "Exit_Coordinate_X_Y" ] ,
                    },
                )
                if created:
                    imported = imported + 1
                else:
                    updated = updated + 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {imported} created, {updated} updated."
            )
        )

    def import_station ( self ) :
        csv_path = Path(__file__).resolve().parents[3] / "data" / "station.csv"
        imported = 0
        updated = 0

#         with csv_path.open(newline="", encoding="utf-8") as csv_file:
        with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                station , created = Station.objects.update_or_create(
                    Station_ID = row [ "Station ID" ] ,
                    defaults={
                        "Line_Code" : row[ "Line Code" ] ,
                        "Direction" : row[ "Direction" ] ,
                        "Station_Code" : row[ "Station Code" ] ,
#                         "Station_ID" : row[ "Station ID" ] ,
                        "Chinese_Name" : row[ "Chinese Name" ] ,
                        "English_Name" : row[ "English Name" ] ,
                        "Sequence" : row[ "Sequence" ] ,
                    },
                )
                if created:
                    imported = imported + 1
                else:
                    updated = updated + 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {imported} created, {updated} updated."
            )
        )

    def import_fare ( self ) :
        csv_path = Path(__file__).resolve().parents[3] / "data" / "fare.csv"
        imported = 0
        updated = 0

#         with csv_path.open(newline="", encoding="utf-8") as csv_file:
        with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                #
                # Create the departing ( source )
                # and destination station instance
                #
                source_station = Station.objects.get ( Station_ID = row [ "SRC_STATION_ID" ] ) ,
                dest_station = Station.objects.get ( Station_ID = row [ "DEST_STATION_ID" ] ) ,

                fare , created = Fare.objects.update_or_create(
                    Source_Station = source_station [ 0 ] ,
                    Destination_Station = dest_station [ 0 ] ,
                    defaults={
                        "Octopus_Card_Adult" : row[ "OCT_ADT_FARE" ] ,
                        "Octopus_Card_Student" : row[ "OCT_STD_FARE" ] ,
                        "Octopus_Card_60" : row[ "OCT_JOYYOU_SIXTY_FARE" ] ,
                        "Single_Ticket" : row[ "SINGLE_ADT_FARE" ] ,
                        "Octopus_Card_Children" : row[ "OCT_CON_CHILD_FARE" ] ,
                        "Octopus_Card_Elderly" : row[ "OCT_CON_ELDERLY_FARE" ] ,
                        "Octopus_Card_Disabled" : row[ "OCT_CON_PWD_FARE" ] ,
                        "Single_Ticket_Children" : row[ "SINGLE_CON_CHILD_FARE" ] ,
                        "Single_Ticket_Elderly" : row[ "SINGLE_CON_ELDERLY_FARE" ] ,
                    },
                )
                if created:
                    imported = imported + 1
                else:
                    updated = updated + 1


        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {imported} created, {updated} updated."
            )
        )

    def handle(self, *args, **options):

        self.import_barrcat ( )
        self.import_station ( )
        self.import_barrfac ( )
        self.import_fare ( )


