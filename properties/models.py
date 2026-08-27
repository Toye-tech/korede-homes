from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class PropertyType(models.Model):
    name = models.CharField(max_length=50)  # e.g. Land, Bungalow, Duplex, Apartment

    class Meta:
        verbose_name_plural = 'Property types'

    def __str__(self):
        return self.name


class Location(models.Model):
    state = models.CharField(max_length=80)
    city = models.CharField(max_length=80)

    class Meta:
        ordering = ['state', 'city']

    def __str__(self):
        return f'{self.city}, {self.state}'


class Agent(models.Model):
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='agents/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold Out'),
        ('coming_soon', 'Coming Soon'),
    ]
    LISTING_CHOICES = [
        ('sale', 'For Sale'),
        ('lease', 'For Lease'),
        ('installment', 'Installment Plan'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, blank=True)

    price = models.DecimalField(max_digits=14, decimal_places=2)
    listing_type = models.CharField(max_length=20, choices=LISTING_CHOICES, default='sale')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    size_sqm = models.PositiveIntegerField(help_text='Size in square metres', default=0)

    description = models.TextField()
    cover_image = models.ImageField(upload_to='properties/covers/', blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='properties/gallery/')
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'Image for {self.property.title}'


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    client_location = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.client_name


class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='inquiries')
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f'Inquiry from {self.full_name}'

class Service(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(max_length=10, default='🏠', help_text='Emoji icon, e.g. 🏠')
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:service-detail', kwargs={'slug': self.slug})


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('buying', 'Buying Process'),
        ('payment', 'Payments & Plans'),
        ('titles', 'Titles & Documentation'),
        ('general', 'General'),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question