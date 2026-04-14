from django.db import connection
from django.shortcuts import redirect
import datetime
import threading  # New import for speed
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import ProjectInquiryForm
from .models import Testimonial
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .models import Project
from .forms import ProjectMessageForm
from django.contrib import messages
# Boking Systems
import threading

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# <--- Crucial: Capital letters for Classes
from .models import Booking, Service


# SEO ROBOT ENTRY INOT THE WEBSITE

#  SEO
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",      # Hide your admin login from search results
        "Disallow: /login/",      # Hide login pages
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ----------------- Home Page -----------------

class HomePage(TemplateView):
    template_name = "CoreApp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Fetch the data
        # 2. Assign it to the context dictionary so the template can find it
        context['testimonials'] = Testimonial.objects.filter(
            is_featured=True).order_by('-created_at')[:3]
        context['projects'] = Project.objects.all()

        return context

# ----------------- Future Project Page -----------------


class FutureProject(TemplateView):
    template_name = "CoreApp/future_project.html"


# ----------------- About Us Page -----------------
class AboutUs(TemplateView):
    template_name = "CoreApp/about.html"


# ----------------- PRoject  -----------------

class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 6

# ----------------- Project Detail -----------------


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    previous_project = Project.objects.filter(
        id__lt=project.id).order_by('-id').first()
    next_project = Project.objects.filter(
        id__gt=project.id).order_by('id').first()

    form = ProjectMessageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.project = project
        msg.save()
        messages.success(request, "Message sent successfully!")
        return redirect('project_detail', slug=project.slug)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'form': form,
        'previous_project': previous_project,
        'next_project': next_project,
        'projects': Project.objects.all(),  # for sidebar
    })


def services_page(request):
    return render(request, "CoreApp/Services.html")


def contact_view(request):
    if request.method == 'POST':
        form = ProjectInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # In your contact_view inside views.py
            if request.headers.get('HX-Request'):
                return render(request, 'booking/partials/success_message.html', {
                    'inquiry': inquiry,
                    # We don't pass date/slot here because they aren't in this form anymore!
                })

        else:
            if request.headers.get('HX-Request'):
                return render(request, 'booking/partials/form_fragment.html', {'form': form})
    else:
        form = ProjectInquiryForm()

    return render(request, 'CoreApp/contact.html', {'form': form})


# BOOKING SYSTEMS

def get_available_slots(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'slots': []})

    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'slots': []})

    # Define business hours
    all_slots = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]

    # Find slots already taken
    booked_slots = Booking.objects.filter(
        booking_date=selected_date
    ).values_list('booking_slot', flat=True)

    booked_slots_str = [slot.strftime('%H:%M') for slot in booked_slots]
    available = [slot for slot in all_slots if slot not in booked_slots_str]

    return JsonResponse({'slots': available})

# 2. The session booking logic


def booking_page(request):
    # This line was likely failing because 'Service' was imported as a function
    services_list = Service.objects.filter(is_active=True)

    return render(request, 'booking/booking_page.html', {
        'today': datetime.date.today(),
        'services': services_list,
    })


def book_session(request):
    if request.method == "POST":
        date = request.POST.get('date')
        slot = request.POST.get('slot')
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        service_id = request.POST.get('service_type')

        # 1. Validate required fields
        if not all([date, slot, name, email, phone, service_id]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        # 2. Validate and convert date
        try:
            booking_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid date format.'
            })

        # 3. Optional but smart: prevent past bookings
        if booking_date < datetime.date.today():
            return JsonResponse({
                'status': 'error',
                'message': 'You cannot book a past date.'
            })

        # 4. Get service safely
        service_obj = get_object_or_404(Service, id=service_id)

        # 5. Check availability (USE validated date)
        if Booking.objects.filter(
            booking_date=booking_date,
            booking_slot=slot
        ).exists():
            return JsonResponse({'status': 'error', 'message': 'This slot was just taken!'})

        try:
            booking = Booking.objects.create(
                full_name=name,
                email=email,
                phone_number=phone,
                service_type=service_obj,
                booking_date=booking_date,  # ✅ FIXED
                booking_slot=slot
            )

            # 6. Background email (still okay for now)
            email_thread = threading.Thread(
                target=send_safe_email,
                args=(booking,)
            )
            email_thread.start()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Database error: {str(e)}'
            })
        finally:
            connection.close()

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
# Helper function to handle email in the background safely


def send_safe_email(booking):
    try:
        send_booking_confirmation(booking)
    except Exception as e:
        print(f"Background email failed: {e}")
# 3. The email trigger


# def send_booking_confirmation(booking):
#     subject = f"Confirmed: Consultation with Aylumlimited"
#     recipient_list = [booking.email]

#     # This context passes data to your HTML email template
#     context = {
#         'name': booking.full_name,
#         'date': booking.booking_date,
#         'time': booking.booking_slot,
#         'service': booking.service_type.name,
#         'token': booking.reschedule_token,
#         'meeting_link': 'https://meet.zoho.com/ocwp-tcg-sdr'
#     }

#     # Render the HTML version of the email
#     html_content = render_to_string('emails/booking_confirmed.html', context)
#     text_content = f"Hi {booking.full_name}, your {booking.service_type.name} session is confirmed for {booking.booking_date}."

#     msg = EmailMultiAlternatives(
#         subject,
#         text_content,
#         'aao@aylumlimited.com',  # Replace with your verified sender email
#         recipient_list,
#     )
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

def send_booking_confirmation(booking):
    subject = "Confirmed: Consultation with Aylum Limited"  # Space added
    recipient_list = [booking.email]

    context = {
        'name': booking.full_name,
        'date': booking.booking_date,
        'time': booking.booking_slot,
        'service': booking.service_type.name,
        'token': booking.reschedule_token,
        # Use your domain redirect here for a cleaner look
        'meeting_link': 'https://aylumlimited.com/join/'
    }

    # Render HTML
    html_content = render_to_string('emails/booking_confirmed.html', context)
    # Plain text version for safety
    text_content = (
        f"Hi {booking.full_name}, your {booking.service_type.name} session is confirmed "
        f"for {booking.booking_date} at {booking.booking_slot}. "
        f"Join here: https://aylumlimited.com/join/"
    )

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        'aao@aylumlimited.com',
        recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def reschedule_booking(request, token):
    # 1. Find the booking using the secure UUID token
    booking = get_object_or_404(Booking, reschedule_token=token)

    if request.method == "POST":
        new_date = request.POST.get('date')
        new_slot = request.POST.get('slot')

        # 2. Update the existing booking record
        booking.booking_date = new_date
        booking.booking_slot = new_slot
        booking.save()

        # 3. Send a fresh confirmation email with the new details
        try:
            send_booking_confirmation(booking)
        except Exception as e:
            print(f"Reschedule email failed: {e}")

        return render(request, 'booking/success_reschedule.html', {
            'booking': booking
        })

    # If GET, show the reschedule page (similar to your booking page)
    return render(request, 'booking/reschedule_form.html', {
        'booking': booking,
        'today': datetime.date.today()
    })


# Add this view to handle the clean redirect

def meeting_redirect(request):
    """Redirects clients directly to the Zoho Meeting room."""
    return redirect('https://meet.zoho.com/ocwp-tcg-sdr')


def testimonials_view(request):
    # Standard view for displaying approved testimonials
    testimonials = Testimonial.objects.filter(
        is_featured=True).order_by('-created_at')

    context = {
        'testimonials': testimonials,
    }
    return render(request, 'CoreApp/testimonias.html', context)


def submit_testimonial(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        content = request.POST.get('content')

        # Safe integer conversion for the star rating
        try:
            stars = int(request.POST.get('stars', 5))
        except (ValueError, TypeError):
            stars = 5

        image = request.FILES.get('image')

        # Validation: Ensure critical data exists
        if not name or not content:
            messages.error(
                request, "Please provide your name and your feedback message.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Create the testimonial: Cloudinary handles the 'image' upload automatically
        Testimonial.objects.create(
            name=name,
            position=position if position else "Valued Client",
            content=content,
            stars=stars,
            image=image,
            is_featured=False  # Hidden until Admin approval
        )

        messages.success(
            request, "Success! Your review has been submitted to Aylum Limited for quality review.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')


def legal_view(request, policy_type):
    # Convert slug like 'terms-of-service' to a nice Title
    title = policy_type.replace('-', ' ').title()

    context = {
        'policy_type': policy_type,
        'title': title,
    }
    return render(request, 'legal.html', context)
