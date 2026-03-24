import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from mtrfare.models import BarrCat , BarrFac , Station , Fare

class Command(BaseCommand):
    help = "Import data from the offline CSV dataset."

    def import_barrcat ( self ) :
        csv_path = Path(__file__).resolve().parents[3] / "data" / "barrcat.csv"
        imported = 0
        updated = 0

        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                barrcat , created = BarrCat.objects.update_or_create(
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

        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                barrfac , created = BarrFac.objects.update_or_create(
                    defaults={
                        "Station_No" : int ( row[ "Station_No" ] ) ,
                        "Key" : row[ "Key" ] ,
                        "Value" : row[ "Value" ]  == "Y" ,
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

        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                station , created = Station.objects.update_or_create(
                    defaults={
                        "Line_Code" : row[ "Line_Code" ] ,
                        "Direction" : row[ "Direction" ] ,
                        "Station_Code" : row[ "Station_Code" ] ,
                        "Station_ID" : row[ "Station_ID" ] ,
                        "Chinese_Name" : row[ "Chinese_Name" ] ,
                        "English_Name" : row[ "English_Name" ] ,
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

        with csv_path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                fare , created = Fare.objects.update_or_create(
                    defaults={
                        "Source_Station_Name" : row[ "Source_Station_Name" ] ,
                        "Source_Station_ID" : int ( row[ "Source_Station_ID" ] ) ,
                        "Destination_Station_Name" : row[ "Destination_Station_Name" ] ,
                        "Destination_Station_ID" : int ( row[ "Destination_Station_ID" ] ) ,
                        "Octopus_Card_Adult" : row[ "Octopus_Card_Adult" ] ,
                        "Octopus_Card_Student" : row[ "Octopus_Card_Student" ] ,
                        "Octopus_Card_60" : row[ "Octopus_Card_60" ] ,
                        "Single_Ticket" : row[ "Single_Ticket" ] ,
                        "Octopus_Card_Children" : row[ "Octopus_Card_Children" ] ,
                        "Octopus_Card_Elderly" : row[ "Octopus_Card_Elderly" ] ,
                        "Octopus_Card_Disabled" : row[ "Octopus_Card_Disabled" ] ,
                        "Single_Ticket_Children" : row[ "Single_Ticket_Children" ] ,
                        "Single_Ticket_Elderly" : row[ "Single_Ticket_Elderly" ] ,
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
        self.import_barrfac ( )
        self.import_station ( )
        self.import_fare ( )


