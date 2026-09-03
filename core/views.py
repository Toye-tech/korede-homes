from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

import logging
logger = logging.getLogger(__name__)
from properties.models import Property, Testimonial, PropertyType, Location, Service, FAQ
from properties.forms import InquiryForm


def home(request):
    context = {
        'featured_properties': Property.objects.filter(is_featured=True, status='available')[:6],
        'latest_properties': Property.objects.filter(status='available')[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'property_types': PropertyType.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            try:
                send_mail(
                    subject=f"New Inquiry from {inquiry.full_name}",
                    message=(
                        f"Name: {inquiry.full_name}\n"
                        f"Email: {inquiry.email}\n"
                        f"Phone: {inquiry.phone}\n\n"
                        f"Message:\n{inquiry.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Contact form email failed: {e}", exc_info=True)
            messages.success(request, "Thank you for reaching out! We'll get back to you shortly.")
            return redirect('core:contact')
    else:
        form = InquiryForm()
    return render(request, 'core/contact.html', {'form': form})


def services(request):
    services_qs = Service.objects.filter(is_active=True)
    return render(request, 'core/services.html', {'services': services_qs})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'core/service_detail.html', {'service': service})


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'core/faq.html', {'faqs': faqs})
