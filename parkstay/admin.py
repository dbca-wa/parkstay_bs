from django.contrib.gis import admin
from parkstay import models

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.db.models import Q

from ledger.accounts.models import EmailUser
from copy import deepcopy

@admin.register(models.CampsiteClass)
class CampsiteClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(models.Park)
class ParkAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'district')
    ordering = ('name',)
    list_filter = ('district',)
    search_fields = ('name',)
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'


@admin.register(models.Campground)
class CampgroundAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'park', 'promo_area', 'campground_type', 'site_type', 'max_advance_booking')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('campground_type', 'site_type')
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'


@admin.register(models.CampgroundGroup)
class CampgroundGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members', 'campgrounds')

    # Added based on moorings to speed up admin site

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(CampgroundGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        """ Filter based on the group of the user"""
        qs = super(CampgroundGroupAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        group = models.CampgroundGroup.objects.filter(members__in=[request.user,])
        return qs.filter(id__in=group)


@admin.register(models.Campsite)
class CampsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'campground',)
    ordering = ('name',)
    list_filter = ('campground',)
    search_fields = ('name',)


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ('name',)


class BookingInvoiceInline(admin.TabularInline):
    model = models.BookingInvoice
    extra = 0


class CampsiteBookingInline(admin.TabularInline):
    model = models.CampsiteBooking
    extra = 0


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    raw_id_fields = ('customer','overridden_by','canceled_by',)
    list_display = ('id','arrival', 'departure', 'campground', 'legacy_id', 'legacy_name', 'cost_total')
    ordering = ('-id',)
    search_fileds = ('arrival', 'departure')
    list_filter = ('arrival', 'departure', 'campground')
    inlines = [BookingInvoiceInline, CampsiteBookingInline]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.CampsiteBooking)
class CampsiteBookingAdmin(admin.ModelAdmin):
    list_display = ('campsite', 'date', 'booking', 'booking_type')
    ordering = ('-date',)
    search_fields = ('date',)
    list_filter = ('campsite', 'booking_type')


@admin.register(models.CampsiteRate)
class CampsiteRateAdmin(admin.ModelAdmin):
    list_display = ('campsite', 'rate', 'allow_public_holidays')
    list_filter = ('campsite', 'rate', 'allow_public_holidays')
    search_fields = ('campground__name',)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    search_fields = ('name', 'phone_number')


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('code', 'text', 'editable')
    search_fields = ('code', 'text')
    readonly_fields = ('code',)

    def get_readonly_fields(self, request, obj=None):
        fields = list(self.readonly_fields)
        if obj and not obj.editable:
            fields += ['text', 'editable']
        elif not obj:
            fields = []
        return fields

    def has_add_permission(self, request, obj=None):
        if obj and not obj.editable:
            return False
        return super(ReasonAdmin, self).has_delete_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.editable:
            return False
        return super(ReasonAdmin, self).has_delete_permission(request, obj)


@admin.register(models.MaximumStayReason)
class MaximumStayReason(ReasonAdmin):
    pass


@admin.register(models.PriceReason)
class PriceReason(ReasonAdmin):
    pass


@admin.register(models.ClosureReason)
class ClosureReason(ReasonAdmin):
    pass


@admin.register(models.OutstandingBookingRecipient)
class OutstandingBookingRecipient(admin.ModelAdmin):
    pass


@admin.register(models.PromoArea)
class PromoAreaAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'wkb_geometry')
    ordering = ('name',)
    search_fields = ('name',)
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'


admin.site.register(models.Rate)
admin.site.register(models.Region)
admin.site.register(models.District)
admin.site.register(models.DiscountReason)
