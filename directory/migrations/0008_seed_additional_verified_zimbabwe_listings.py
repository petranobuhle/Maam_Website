import datetime

from django.db import migrations


VERIFIED_AT = datetime.datetime(2026, 11, 17, tzinfo=datetime.timezone.utc)


def add_verified_organisation(Organisation, SupportService, country, data):
    organisation, created = Organisation.objects.get_or_create(
        slug=data["slug"],
        defaults={
            "name": data["name"],
            "country": country,
            "city": data.get("city", ""),
            "address": data.get("address", ""),
            "website": data["website"],
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
            "description": data["description"],
            "verification_source": data["source"],
            "is_verified": True,
            "is_demo": False,
            "verification_status": "verified",
            "last_verified_at": VERIFIED_AT,
        },
    )
    if not created:
        return

    for service in data["services"]:
        SupportService.objects.get_or_create(
            organisation=organisation,
            name=service["name"],
            defaults={
                "country": country,
                "service_type": service["service_type"],
                "delivery_mode": service.get("delivery_mode", "not_stated"),
                "description": service["description"],
                "intended_for": service.get("intended_for", ""),
                "languages": "",
                "operating_hours": service.get("operating_hours", ""),
                "whatsapp_url": service.get("whatsapp_url", ""),
                "city": service.get("city", ""),
                "phone": "",
                "email": "",
                "website": service.get("website", ""),
                "verification_source": service["source"],
                "is_verified": True,
                "verification_status": "verified",
                "last_verified_at": VERIFIED_AT,
                "is_demo": False,
                "is_active": True,
            },
        )


def seed_additional_listings(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    Organisation = apps.get_model("directory", "Organisation")
    SupportService = apps.get_model("directory", "SupportService")
    country = Country.objects.filter(code="ZW", is_active=True).first()
    if country is None:
        return

    listings = [
        {
            "slug": "freshstart-mental-health-support-organisation",
            "name": "FreshStart Mental Health Support Organisation",
            "city": "Harare",
            "address": "117–119 Brunok Building, Rotten Row, Harare",
            "website": "https://freshstartngo.org/",
            "phone": "+263 78 899 5400 / +263 71 340 3415",
            "description": (
                "FreshStart describes its work as providing mental health support "
                "to communities across Zimbabwe, including psychosocial support, "
                "peer groups and mental health education."
            ),
            "source": "https://freshstartngo.org/contact.html",
            "services": [
                {
                    "name": "Professional psychosocial support",
                    "service_type": "Direct mental health and psychosocial support",
                    "delivery_mode": "in_person",
                    "description": (
                        "FreshStart lists individual and family psychosocial support, "
                        "including referral services. Its official services page does "
                        "not confirm that every service is offered at every location."
                    ),
                    "operating_hours": (
                        "Office hours: Monday–Thursday, 8:30am–4:30pm; "
                        "Friday, 8:30am–1pm; Saturday by appointment; Sunday closed."
                    ),
                    "website": "https://freshstartngo.org/services.html",
                    "source": "https://freshstartngo.org/services.html",
                },
                {
                    "name": "Community peer support groups",
                    "service_type": "Direct peer support",
                    "delivery_mode": "community",
                    "description": (
                        "FreshStart describes peer-led support groups where people "
                        "can share experiences, learn coping strategies and connect."
                    ),
                    "website": "https://freshstartngo.org/services.html",
                    "source": "https://freshstartngo.org/services.html",
                },
                {
                    "name": "Mental health education",
                    "service_type": "Mental health education",
                    "delivery_mode": "community",
                    "description": (
                        "FreshStart lists workshops, school programmes, workplace "
                        "seminars and educational materials intended to increase "
                        "mental health awareness."
                    ),
                    "website": "https://freshstartngo.org/services.html",
                    "source": "https://freshstartngo.org/services.html",
                },
            ],
        },
        {
            "slug": "happy-nest-counselling-chambers",
            "name": "Happy Nest Counselling Chambers",
            "city": "Masvingo, Harare, Gweru, Bulawayo, Zvishavane and Shurugwi",
            "address": (
                "Published offices include Masvingo, Harare, Gweru, Bulawayo, "
                "Zvishavane and Shurugwi."
            ),
            "website": "https://www.hncc.org.zw/",
            "phone": "+263 777 757 958",
            "email": "admin@hncc.org.zw",
            "description": (
                "Happy Nest Counselling Chambers describes itself as a professional "
                "counselling service. The organisation lists offices in several "
                "cities; availability of each service at each office is not stated."
            ),
            "source": "https://www.hncc.org.zw/contact/",
            "services": [
                {
                    "name": "Counselling services",
                    "service_type": "Direct mental health support",
                    "delivery_mode": "hybrid",
                    "description": (
                        "The official services page lists individual, couples, family, "
                        "group and online counselling. Confirm service and location "
                        "availability directly with the organisation."
                    ),
                    "website": "https://www.hncc.org.zw/services/",
                    "source": "https://www.hncc.org.zw/services/",
                },
                {
                    "name": "Therapeutic interventions",
                    "service_type": "Counselling and therapeutic support",
                    "delivery_mode": "not_stated",
                    "description": (
                        "The official site lists psychological assessment and diagnosis, "
                        "therapeutic interventions and other counselling-related services. "
                        "Availability at each office is not stated."
                    ),
                    "website": "https://www.hncc.org.zw/services/",
                    "source": "https://www.hncc.org.zw/services/",
                },
                {
                    "name": "Development, education and training",
                    "service_type": "Mental health education and training",
                    "delivery_mode": "community",
                    "description": (
                        "The organisation lists workshops, training and educational "
                        "programmes for communities, schools and workplaces."
                    ),
                    "website": "https://www.hncc.org.zw/services/",
                    "source": "https://www.hncc.org.zw/services/",
                },
            ],
        },
        {
            "slug": "anxiety-support-and-awareness-centre",
            "name": "Anxiety Support and Awareness Centre (ASAC)",
            "website": "https://asactrust.co.zw/",
            "phone": "+263 719 555 772",
            "email": "asactrust.org@gmail.com",
            "description": (
                "ASAC describes work in mental health support and awareness. Its "
                "official pages list counselling, support groups, community outreach "
                "and advocacy."
            ),
            "source": "https://asactrust.co.zw/get-help/",
            "services": [
                {
                    "name": "Counselling and published support contact",
                    "service_type": "Direct mental health support",
                    "delivery_mode": "phone",
                    "description": (
                        "ASAC's get-help page publishes a phone and WhatsApp contact "
                        "for people seeking help or wishing to book a counselling "
                        "session. No response time is stated here."
                    ),
                    "source": "https://asactrust.co.zw/get-help/",
                },
                {
                    "name": "Tariro support groups",
                    "service_type": "Direct peer support",
                    "delivery_mode": "community",
                    "description": (
                        "Tariro Support Groups are listed among ASAC's offerings. "
                        "Contact ASAC to confirm current group arrangements."
                    ),
                    "website": "https://asactrust.co.zw/",
                    "source": "https://asactrust.co.zw/",
                },
                {
                    "name": "Mental health awareness and community outreach",
                    "service_type": "Mental health advocacy and education",
                    "delivery_mode": "community",
                    "description": (
                        "ASAC lists mental health awareness, public outreach, "
                        "workshops and advocacy among its activities."
                    ),
                    "website": "https://asactrust.co.zw/",
                    "source": "https://asactrust.co.zw/",
                },
            ],
        },
        {
            "slug": "connect-zimbabwe-institute-of-systemic-therapy",
            "name": "Connect Zimbabwe Institute of Systemic Therapy (CONNECT-ZIST)",
            "city": "Harare",
            "address": (
                "18149 Ganges Road, Cnr Convair, Ridgeview, Belvedere, Harare"
            ),
            "website": "https://connect.org.zw/",
            "phone": (
                "0242 741719 / 0242 741779 / 0242 741726 / 0242 741794"
            ),
            "email": "admin@connect.org.zw",
            "description": (
                "CONNECT-ZIST describes itself as a welfare organisation offering "
                "counselling, therapy, training and consultancy to individuals, "
                "families, organisations and communities."
            ),
            "source": "https://connect.org.zw/contact/",
            "services": [
                {
                    "name": "Individual, couples and family counselling",
                    "service_type": "Direct mental health support",
                    "delivery_mode": "in_person",
                    "description": (
                        "The organisation lists individual, couples and family "
                        "counselling and therapy. Its contact page publishes weekday "
                        "office hours; confirm current arrangements directly."
                    ),
                    "operating_hours": "Office hours: Monday–Friday, 8:30am–4:00pm",
                    "whatsapp_url": "https://wa.me/263778914501",
                    "website": "https://connect.org.zw/",
                    "source": "https://connect.org.zw/",
                },
                {
                    "name": "Training and consultancy",
                    "service_type": "Mental health training and consultancy",
                    "delivery_mode": "not_stated",
                    "description": (
                        "CONNECT-ZIST lists training and consultancy services. "
                        "Contact the organisation for current programme details."
                    ),
                    "website": "https://connect.org.zw/",
                    "source": "https://connect.org.zw/",
                },
            ],
        },
        {
            "slug": "phoebe-centre-zimbabwe",
            "name": "Phoebe Centre Zimbabwe",
            "city": "Harare",
            "address": "136 Coronation Avenue, Greendale, Harare, Zimbabwe",
            "website": "https://phoebecentre.org/",
            "phone": "(024) 2448060 / +263 71 658 6831 / +263 77 965 1691",
            "email": "adminzim@phoebecentre.org.uk",
            "description": (
                "Phoebe Centre describes work supporting women and girls with mental "
                "health conditions, helping them access care and supporting caregivers."
            ),
            "source": "https://phoebecentre.org/contact-us/",
            "services": [
                {
                    "name": "Psychological support and counselling",
                    "service_type": "Psychological support and counselling",
                    "delivery_mode": "in_person",
                    "description": (
                        "The organisation describes individual and group counselling, "
                        "caregiver support and assistance accessing care."
                    ),
                    "intended_for": (
                        "Women and girls with mental health conditions, and their "
                        "caregivers, as described by Phoebe Centre."
                    ),
                    "website": "https://phoebecentre.org/psychological-support/",
                    "source": "https://phoebecentre.org/psychological-support/",
                },
            ],
        },
        {
            "slug": "ndinewe-foundation",
            "name": "Ndinewe Foundation",
            "city": "Harare",
            "address": "322 off Beeston Avenue, The Grange, Harare, Zimbabwe",
            "website": "https://ndinewe.org/",
            "phone": "+263 781 293888",
            "email": "info@ndinewe.org",
            "description": (
                "Ndinewe describes itself as a youth mental health organisation "
                "working through research, education, advocacy and sustainable "
                "interventions in Zimbabwe."
            ),
            "source": "https://ndinewe.org/about-us",
            "services": [
                {
                    "name": "Youth mental health education and resources",
                    "service_type": "Mental health education",
                    "delivery_mode": "community",
                    "description": (
                        "Ndinewe lists mental health education and awareness in "
                        "schools, rural communities, workplaces and prisons. Its "
                        "website also publishes a mental health course and educational "
                        "resources."
                    ),
                    "website": "https://ndinewe.org/",
                    "source": "https://ndinewe.org/",
                },
                {
                    "name": "Mental health research and advocacy",
                    "service_type": "Mental health advocacy and education",
                    "delivery_mode": "not_stated",
                    "description": (
                        "The organisation describes research as a core pillar of its "
                        "work and lists mental health advocacy and awareness."
                    ),
                    "website": "https://ndinewe.org/about-us",
                    "source": "https://ndinewe.org/about-us",
                },
            ],
        },
        {
            "slug": "tree-of-life-trust-zimbabwe",
            "name": "Tree of Life Trust Zimbabwe",
            "city": "Harare and Bulawayo; programmes across 8 of 10 provinces",
            "website": "https://www.treeoflifezimbabwe.org/",
            "description": (
                "Tree of Life describes community-based mental health and psychosocial "
                "support, trauma healing and social cohesion work. Its website lists "
                "offices in Harare and Bulawayo and programmes in eight of Zimbabwe's "
                "ten provinces."
            ),
            "source": "https://www.treeoflifezimbabwe.org/node/59",
            "services": [
                {
                    "name": "Community mental health and psychosocial support",
                    "service_type": "Direct mental health and psychosocial support",
                    "delivery_mode": "community",
                    "description": (
                        "Tree of Life describes evidence-based, community-rooted "
                        "mental health and psychosocial support for people living "
                        "with trauma and other difficulties."
                    ),
                    "website": "https://www.treeoflifezimbabwe.org/node/59",
                    "source": "https://www.treeoflifezimbabwe.org/node/59",
                },
                {
                    "name": "Trauma healing and resilience building",
                    "service_type": "Community-based trauma support",
                    "delivery_mode": "community",
                    "description": (
                        "The organisation lists Trauma Healing and Empowerment "
                        "workshops and community resilience activities."
                    ),
                    "website": "https://www.treeoflifezimbabwe.org/node/59",
                    "source": "https://www.treeoflifezimbabwe.org/node/59",
                },
                {
                    "name": "Psychoeducation and social cohesion",
                    "service_type": "Mental health education and community development",
                    "delivery_mode": "community",
                    "description": (
                        "Tree of Life lists psychoeducation, community facilitator "
                        "training and social cohesion work. This listing is not an "
                        "emergency or walk-in clinic service."
                    ),
                    "website": "https://www.treeoflifezimbabwe.org/",
                    "source": "https://www.treeoflifezimbabwe.org/",
                },
            ],
        },
        {
            "slug": "contact-family-counselling-centre",
            "name": "CONTACT Family Counselling Centre",
            "city": "Bulawayo",
            "address": "9 Barbour Avenue, Parkview, Bulawayo, Zimbabwe",
            "website": "https://contactfcc.co.zw/",
            "phone": "+263 29 2272400 / +263 29 2881842",
            "email": "contact@contactfcc.co.zw",
            "description": (
                "CONTACT Family Counselling Centre describes counselling, training "
                "and child protection support for individuals, families and communities."
            ),
            "source": "https://contactfcc.co.zw/",
            "services": [
                {
                    "name": "Individual and family counselling",
                    "service_type": "Direct mental health support",
                    "delivery_mode": "in_person",
                    "description": (
                        "The centre describes individual and family counselling."
                    ),
                    "website": "https://contactfcc.co.zw/",
                    "source": "https://contactfcc.co.zw/",
                },
                {
                    "name": "Counselling training",
                    "service_type": "Counselling training",
                    "delivery_mode": "not_stated",
                    "description": (
                        "The centre lists training programmes to build counselling "
                        "knowledge and skills among community and sector workers."
                    ),
                    "website": "https://contactfcc.co.zw/",
                    "source": "https://contactfcc.co.zw/",
                },
                {
                    "name": "Child protection support",
                    "service_type": "Child protection and family support",
                    "delivery_mode": "not_stated",
                    "description": (
                        "The centre describes child protection case management and "
                        "support for children and their families."
                    ),
                    "website": "https://contactfcc.co.zw/",
                    "source": "https://contactfcc.co.zw/",
                },
            ],
        },
    ]

    for listing in listings:
        add_verified_organisation(Organisation, SupportService, country, listing)


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0007_organisation_phone"),
        ("core", "0002_seed_country_language_data"),
    ]

    operations = [
        migrations.RunPython(seed_additional_listings, migrations.RunPython.noop),
    ]
