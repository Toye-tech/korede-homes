# Korede Homes and Properties — Django Website

A responsive, mobile-friendly real estate website built with **Python/Django**
and **Supabase (Postgres)** as the database, competing directly with sites like
Adron Homes: property listings with search/filter, property detail pages with
an inquiry form, agent profiles, testimonials, and an admin dashboard for
managing everything without touching code.

## Features
- Home page: hero, quick search, featured listings, "why choose us", testimonials, CTA
- Property listing page with search + filters (type, location, listing type) + pagination
- Property detail page with gallery, key facts, agent card, inquiry form
- About & Contact pages with a working contact form
- Fully responsive (desktop, tablet, mobile) — custom CSS, no bloated framework
- Django Admin for managing properties, images, agents, testimonials, inquiries
- Ready for Supabase Postgres via a single `DATABASE_URL` env var

## 1. Open in PyCharm
1. `File > Open` and select this `korede_homes` folder.
2. PyCharm will detect it as a Django project. If prompted, set the Django
   support settings: Settings root = this folder, settings file =
   `korede_project/settings.py`.

## 2. Create a virtual environment
In PyCharm's terminal (or Settings > Python Interpreter > Add Interpreter):

```bash
python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Set up Supabase as your database
1. Create a free project at https://supabase.com.
2. In your Supabase project: **Project Settings > Database > Connection string > URI**.
   Copy the connection string (use the **Session pooler** URI — port `6543` — for
   most reliable connections from a normal Django app).
3. Copy `.env.example` to `.env` and paste your values:

```
SECRET_KEY=some-long-random-string
DEBUG=True
DATABASE_URL=postgresql://postgres.xxxxxxxx:YOUR-PASSWORD@aws-0-region.pooler.supabase.com:6543/postgres
```

`settings.py` reads `DATABASE_URL` automatically via `dj-database-url`. If you
don't set it, the project falls back to local SQLite so you can still run it
immediately.

## 4. Run migrations & create an admin user
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 5. (Optional) Load demo content
```bash
python manage.py seed_demo_data
```
This creates sample property types, locations, an agent, six sample
properties and testimonials so the site isn't empty. Add real cover images
for each property afterwards from `/admin/`.

## 6. Run the server
```bash
python manage.py runserver
```
Visit:
- `http://127.0.0.1:8000/` — the website
- `http://127.0.0.1:8000/admin/` — manage properties, agents, testimonials, inquiries

## Project structure
```
korede_homes/
├── korede_project/     # settings, root urls
├── core/                # home, about, contact views
├── properties/          # Property, Agent, Testimonial, Inquiry models + views
├── templates/           # base.html, shared includes
├── static/css/style.css # all site styling (custom, responsive)
└── static/js/main.js    # mobile nav + scroll animations
```

## Adding real property images
Go to `/admin/`, open **Properties**, add/edit a listing, and upload a
**Cover image** plus extra **gallery images** (inline at the bottom of the
edit form). Images are stored under `media/` locally — for production, wire
up Supabase Storage or another cloud storage backend (e.g. `django-storages`
with an S3-compatible provider) so uploads persist between deploys.

## Deploying
- Any host that runs Django works (Railway, Render, PythonAnywhere, Fly.io,
  a VPS, etc.) since the database already lives on Supabase.
- Set `DEBUG=False` and a real `ALLOWED_HOSTS` in your production `.env`.
- Run `python manage.py collectstatic` before deploying (Whitenoise serves
  static files in production).

## Next steps you may want
- Add a mortgage/installment calculator widget on property detail pages
- Add a blog app for SEO content, matching competitor sites
- Hook the contact/inquiry forms to send email or WhatsApp notifications
- Add user accounts so clients can track "My Inquiries" / saved properties
