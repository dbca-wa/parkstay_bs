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
from datetime import timedelta
globalcount = 0
class Command(BaseCommand):
    help = 'Rebuild mooring booking property cache.'

    def handle(self, *args, **options):
        print ("current version: " + settings.BOOKING_PROPERTY_CACHE_VERSION)
        try:
           total_uncached_bookings = 1000
           while total_uncached_bookings > 0:
               bookings = models.Booking.objects.exclude(property_cache_version=settings.BOOKING_PROPERTY_CACHE_VERSION).exclude(booking_type=3)
               #.exclude(property_cache_version=settings.BOOKING_PROPERTY_CACHE_VERSION, booking_type=3)
               total_uncached_bookings = bookings.count()
               print ("---==========================---")
               print ("COUNT: "+str(total_uncached_bookings))
               print ("---==========================---")
               globalcount = 0
               bookings = models.Booking.objects.exclude(property_cache_version=settings.BOOKING_PROPERTY_CACHE_VERSION).exclude(booking_type=3).order_by('-id')[:100]
               for b in bookings:
                   t = None
                   try:
                   
                       b.property_cache['cache_version']
                       print (b.property_cache['cache_version'])
                       if b.property_cache_version != settings.BOOKING_PROPERTY_CACHE_VERSION:
                           print ("Rebuilding :"+str(b.id))
                           t = threading.Thread(target=update_cache,args=[b.id,],daemon=False)
                           globalcount = globalcount + 1
                   except:
                        #b.update_property_cache()
                        t = threading.Thread(target=update_cache,args=[b.id,],daemon=False)
                        globalcount = globalcount + 1
                   #if b.property_cache['cache_version'] != settings.BOOKING_PROPERTY_CACHE_VERSION:
                   #     print ("Rebuilding :"+str(b.id))
                   #     t = threading.Thread(target=update_cache,args=[b.id,],daemon=True)
                   #print ('thread')
                   #print (t)
                   if t is not None:
                        if globalcount > 9:
                             print ("Sleeping")      
                             time.sleep(10)
                             globalcount = 0
                        t.start()
               print ("--NEW LOOP--")
               time.sleep(35)
                        #b.update_property_cache()

        except Exception as e:
            print (e)
            #Send fail email
            content = "Error message: {}".format(e)

def update_cache(booking_id):
     print ('New Rebuild for: '+str(booking_id))
     #b= models.Booking.objects.get(id=int(booking_id))
     #b.update_property_cache(True)
     property_cache.update_property_cache(booking_id)
     print ('Finished :'+str(booking_id))


