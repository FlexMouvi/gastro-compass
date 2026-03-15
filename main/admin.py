from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Restaurant, Dish, Review, Tour, TourReview, Profile, Booking

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Профиль"
    verbose_name_plural = "Профили"

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff']
    
    def get_phone(self, obj):
        try:
            return obj.profile.phone
        except Profile.DoesNotExist:
            return '-'
    get_phone.short_description = 'Телефон'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at')
    search_fields = ('name', 'address')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('restaurant',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'rating', 'created_at')
    list_filter = ('rating', 'restaurant')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'duration')
    filter_horizontal = ('restaurants',)

@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'created_at')
    list_filter = ('rating', 'tour')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'tour', 'date', 'guests', 'created_at')
    list_filter = ('tour', 'date')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'created_at'