
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

# BOOKING SYSTEMS
import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):

    CATEGORY_CHOICES = [
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
        ("Institutional", "Institutional"),
    ]

    STATUS_CHOICES = [
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)

    completion_date = models.DateField(null=True, blank=True)

    featured_image = models.ImageField(
        upload_to="projects/", blank=True, null=True)
    featured_video = models.FileField(
        upload_to="projects/videos/", blank=True, null=True)
    secondary_image = models.ImageField(
        upload_to="projects/", blank=True, null=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectMessage(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} on {self.project.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(
        max_length=100, help_text="e.g. CEO of BuildCorp or Homeowner")
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    stars = models.IntegerField(
        default=5, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name.upper()} - {self.position}"


# CONTACT MODELS

class ProjectInquiry(models.Model):
    SERVICE_CHOICES = [
        ('Civil Engineering', 'Civil Engineering'),
        ('Aluminum Fabrication', 'Aluminum Fabrication'),
        ('Curtain Walls', 'Curtain Walls / Cladding'),
        ('Telecommunications', 'Turnkey Cell Site Delivery'),
        ('Consultancy', 'General Consultancy'),
        ('Testimony', 'Testimony'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(
        blank=True, null=True, help_text="Enter number with +country code")
    email = models.EmailField()
    service_category = models.CharField(
        max_length=50, choices=SERVICE_CHOICES, default='Civil Engineering')
    message = models.TextField()

    # Meta data
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(
        default=False, help_text="Mark as checked once you have contacted the client.")
    reference_id = models.CharField(
        max_length=20, editable=False, unique=True, null=True)

    class Meta:
        verbose_name = "Project Inquiry"
        verbose_name_plural = "Project Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.service_category} ({self.created_at.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        # 1. Save first to generate the auto-increment ID
        super().save(*args, **kwargs)

    # 2. If reference_id is empty, create it and save again
        if not self.reference_id:
            self.reference_id = f"INQ-{self.id:04d}"
            # update_fields is efficient and prevents recursion issues
            super().save(update_fields=['reference_id'])


# SERVICE
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# BOOKINY SYSTEMS

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    service_type = models.CharField(max_length=100)

    # The "Real-Time" parts
    booking_date = models.DateField()
    booking_slot = models.TimeField()

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reschedule_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    service_type = models.ForeignKey(
        Service, null=True, on_delete=models.CASCADE)

    class Meta:
        # Prevents double booking the same slot
        unique_together = ('booking_date', 'booking_slot')
        ordering = ['booking_date', 'booking_slot']

    def __str__(self):
        return f"{self.full_name} - {self.booking_date} @ {self.booking_slot}"
