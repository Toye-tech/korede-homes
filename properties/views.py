from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Property, PropertyType, Location
from .forms import InquiryForm


def property_list(request):
    properties = Property.objects.filter(status='available').select_related('property_type', 'location')

    q = request.GET.get('q')
    property_type = request.GET.get('type')
    location = request.GET.get('location')
    listing_type = request.GET.get('listing_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if q:
        properties = properties.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q)
        )
    if property_type:
        properties = properties.filter(property_type_id=property_type)
    if location:
        properties = properties.filter(location_id=location)
    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    paginator = Paginator(properties, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'property_types': PropertyType.objects.all(),
        'locations': Location.objects.all(),
        'request_get': request.GET,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    related = Property.objects.filter(
        property_type=property_obj.property_type, status='available'
    ).exclude(pk=property_obj.pk)[:3]

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property_obj
            inquiry.save()
            messages.success(request, 'Thanks! Your inquiry has been sent. Our team will reach out shortly.')
            return redirect('properties:detail', slug=slug)
    else:
        form = InquiryForm()

    context = {
        'property': property_obj,
        'related_properties': related,
        'form': form,
    }
    return render(request, 'properties/property_detail.html', context)
