from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProjectSitemap


# This For SEO
from .views import robots_txt
sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
}

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("future/", views.FutureProject.as_view(), name="future"),
    path("about/", views.AboutUs.as_view(), name="about"),
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("service/", views.services_page, name="service"),
    path('legal/<slug:policy_type>/', views.legal_view, name='legal_page'),
    # This is the page where people VIEW the testimonials
    path('testimonials/', views.testimonials_view, name='testimonials'),

    # This is a "silent" URL just for PROCESSING the form data
    path('submit-feedback/', views.submit_testimonial, name='submit_testimonial'),
    path('contact/', views.contact_view, name='contact'),


    # BOOKING SYSTEMS
    # The actual page the user visits to start booking
    path('book/', views.booking_page, name='booking_page'),

    # The API endpoints the JavaScript will "talk" to
    path('get-slots/', views.get_available_slots, name='get_slots'),

    path('book-session/', views.book_session, name='book_session'),

    # The unique link for rescheduling (usually sent via email)
    path('reschedule/<uuid:token>/',
         views.reschedule_booking, name='reschedule_booking'),


    # SEO UPTIMISATION
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", robots_txt),

    path('join/', views.meeting_redirect, name='meeting_join'),
]
