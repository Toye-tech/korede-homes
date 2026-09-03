def site_settings(request):
    """Global values available in every template (navbar, footer, contact info)."""
    return {
        'SITE_NAME': 'Korede Homes and Properties',
        'SITE_PHONE': '+234 803 802 1970',
        'SITE_PHONE_2': '+234 807 830 9300',
        'SITE_EMAIL': 'koredeodunayo543@gmail.com',
        'SITE_WHATSAPP': '2348038021970',
        'SITE_ADDRESS': '5 Akanbi Akinpelu close,besides health centre,Oluwo Nla,Basorun, Ibadan, Oyo State, Nigeria',
    }