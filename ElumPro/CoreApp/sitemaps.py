from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Project  # Import your Project model


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        # This assumes you have an 'updated_at' field,
        # otherwise you can skip this method.
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        # List the 'name' of your static URLs here
        return ['home', 'about', 'booking_page', 'portfolio']

    def location(self, item):
        return reverse(item)
