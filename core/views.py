from django.db.models import Q
from django.shortcuts import render

from core.models import Country
from directory.models import SupportService
from education.models import Article


def _get_active_country():
    return Country.objects.filter(is_active=True).order_by("name").first()


def home(request):
    country = _get_active_country()
    articles = Article.objects.filter(
        Q(country=country) | Q(country__isnull=True),
        is_published=True,
        is_demo=False,
    ).order_by("-is_featured", "title")[:3]
    support_services = SupportService.objects.filter(
        country=country,
        is_active=True,
        is_demo=False,
        is_verified=True,
        verification_status="verified",
        organisation__is_demo=False,
        organisation__is_verified=True,
        organisation__verification_status="verified",
    ).select_related("organisation")[:2]
    return render(
        request,
        "core/home.html",
        {
            "articles": articles,
            "support_services": support_services,
            "has_verified_support": support_services.exists(),
            "country": country,
        },
    )


def about(request):
    return render(request, "core/about.html")


def privacy(request):
    return render(request, "core/privacy.html")


def safeguarding(request):
    return render(request, "core/safeguarding.html")


def contact(request):
    return render(request, "core/simple_page.html", {
        "title": "Contact MAAM",
        "eyebrow": "Start a conversation",
        "content": "For general enquiries, email mahwadupetra@gmail.com. You can also use the volunteer and partnership forms to express interest. Please do not send private health information or urgent requests through this educational website.",
        "action_url": "mailto:mahwadupetra@gmail.com",
        "action_label": "Email MAAM",
    })
