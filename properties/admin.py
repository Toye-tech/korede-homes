from django.contrib import admin
from .models import PropertyType, Location, Agent, Property, PropertyImage, Testimonial, Inquiry


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'location', 'price', 'listing_type', 'status', 'is_featured')
    list_filter = ('status', 'listing_type', 'property_type', 'location')
    search_fields = ('title', 'description', 'address')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state')
    list_filter = ('state',)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'phone', 'email')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'is_active')
    list_filter = ('is_active', 'rating')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'property', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


from .models import Service, FAQ

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category']
