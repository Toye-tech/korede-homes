from django.core.management.base import BaseCommand
from properties.models import PropertyType, Location, Agent, Property, Testimonial


class Command(BaseCommand):
    help = 'Populate the database with sample properties, agents and testimonials for demo purposes.'

    def handle(self, *args, **options):
        types = {}
        for name in ['Land', 'Bungalow', 'Duplex', 'Apartment', 'Terrace House']:
            obj, _ = PropertyType.objects.get_or_create(name=name)
            types[name] = obj

        locations = {}
        for city, state in [
            ('Lekki', 'Lagos'), ('Ibeju-Lekki', 'Lagos'), ('Mowe', 'Ogun'),
            ('Epe', 'Lagos'), ('Abuja', 'FCT'), ('Ibadan', 'Oyo'),
        ]:
            obj, _ = Location.objects.get_or_create(city=city, state=state)
            locations[city] = obj

        agent, _ = Agent.objects.get_or_create(
            full_name='Korede Adebayo', role='Senior Property Consultant',
            phone='+2348012345678', email='korede@koredehomes.com'
        )

        sample_properties = [
            ('Emerald Gardens Estate', 'Land', 'Lekki', 8500000, 'installment', True, 0, 0, 500),
            ('Royal Palm Court', 'Bungalow', 'Ibeju-Lekki', 45000000, 'sale', True, 3, 2, 250),
            ('Golden View Duplex', 'Duplex', 'Mowe', 65000000, 'sale', True, 5, 4, 400),
            ('Serenity Apartments', 'Apartment', 'Abuja', 3200000, 'lease', False, 2, 2, 120),
            ('Sunrise Terrace', 'Terrace House', 'Ibadan', 38000000, 'sale', False, 4, 3, 300),
            ('Heritage Land Estate', 'Land', 'Epe', 4500000, 'installment', True, 0, 0, 600),
        ]

        for title, ptype, city, price, listing_type, featured, beds, baths, size in sample_properties:
            Property.objects.get_or_create(
                title=title,
                defaults=dict(
                    property_type=types[ptype], location=locations[city],
                    price=price, listing_type=listing_type, is_featured=featured,
                    bedrooms=beds, bathrooms=baths, size_sqm=size, agent=agent,
                    description=(
                        f'{title} is a premium {ptype.lower()} property located in {city}, '
                        'offering excellent access roads, dry land, and genuine title documents. '
                        'A great investment opportunity with flexible payment options available.'
                    ),
                    cover_image='',
                )
            )

        testimonials = [
            ('Chinedu Okafor', 'Lekki, Lagos', 'Korede Homes made my land purchase so easy. Genuine documents and a smooth process from start to finish!'),
            ('Amaka Johnson', 'Abuja', 'My agent was patient and answered every question. I now own my first property thanks to their installment plan.'),
            ('Tunde Bakare', 'Ibadan, Oyo', 'Professional, transparent and reliable. I recommend Korede Homes to anyone looking to invest in real estate.'),
        ]
        for name, loc, msg in testimonials:
            Testimonial.objects.get_or_create(client_name=name, defaults=dict(client_location=loc, message=msg))

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write(self.style.WARNING(
            'Note: sample properties have no cover image set — add images via /admin/ for them to display correctly.'
        ))
