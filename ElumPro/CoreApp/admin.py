from .models import Booking
from .models import ProjectInquiry
from django.contrib import admin
from .models import Project, Testimonial, Service
# ProjectMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "created_at")
    list_filter = ("category", "status", "is_featured")
    search_fields = ("title", "location")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)

# TESTIMONIA


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'stars', 'is_featured')
    list_filter = ('stars', 'is_featured')
    search_fields = ('name', 'content')


# CONTACT ADMIN
@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    # Display the actual database field 'reference_id'
    list_display = ('reference_id', 'full_name',
                    'service_category', 'created_at', 'is_resolved')

    # This allows you to search by name, email, OR the Inquiry Code
    search_fields = ('reference_id', 'full_name', 'email')

    list_filter = ('service_category', 'is_resolved')

    # Make sure it can't be edited by hand in the admin
    readonly_fields = ('reference_id', 'created_at')


#  SERVICES

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

# BOOKING SYSTEMS


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # What you see in the main list
    list_display = ('full_name', 'booking_date', 'booking_slot',
                    'status', 'service_type', 'created_at')

    # Sidebar filters to find specific days or pending sessions quickly
    list_filter = ('status', 'booking_date', 'service_type')

    # Search by client name or email
    search_fields = ('full_name', 'email', 'phone_number')

    # Organizing the detail view
    fieldsets = (
        ('Client Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Appointment Details', {
            'fields': ('service_type', 'booking_date', 'booking_slot', 'status')
        }),
        ('System Metadata', {
            'classes': ('collapse',),  # Hides this section by default
            'fields': ('reschedule_token', 'created_at'),
        }),
    )

    readonly_fields = ('reschedule_token', 'created_at')
