from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import threading

#from mooring.models import RegisteredVessels
from parkstay import models
from datetime import datetime
import json
import time
from parkstay import property_cache
from parkstay import emails, models
from datetime import timedelta
from datetime import date

class Command(BaseCommand):
    help = 'Send confirmation booking email.'

    def handle(self, *args, **options):

        today = date.today()
        campsite_bookings = []
        cs = models.CampsiteBooking.objects.filter(booking__arrival__gte=today, booking__booking_type__in=[0,1,2]).values('id','booking__booking_type','date','campsite_id','booking__id','booking__is_canceled').order_by('-booking__arrival')
        for c in cs:
             row = {}
             row['id'] = c['id']
             row['booking_type'] = c['booking__booking_type']
             row['date'] = c['date'].strftime('%Y-%m-%d')
             row['campsite_id'] = c['campsite_id']
             row['booking_id'] = c['booking__id']
             row['is_canceled'] = c['booking__is_canceled']
             campsite_bookings.append(row)

        dumped_data = json.dumps(campsite_bookings)
        print ("writing to file")
        f = open("/app/logs/campsite_booking_legacy.json", "w")
        f.write(dumped_data)
        f.close()
