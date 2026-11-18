from django.db.models import Prefetch, Q
from django.shortcuts import render

from core.models import Country
from .models import Organisation, SupportService


def _get_active_country():
    return Country.objects.filter(is_active=True).first()


def support_directory(request):
    country = _get_active_country()
    query = request.GET.get("q", "").strip()[:100]
    verified_services = SupportService.objects.filter(
        country=country,
        is_verified=True,
        verification_status="verified",
        is_demo=False,
        is_active=True,
        organisation__is_verified=True,
        organisation__verification_status="verified",
        organisation__is_demo=False,
    ).select_related("organisation", "country")
    organisations = Organisation.objects.filter(
        country=country,
        is_verified=True,
        verification_status="verified",
        is_demo=False,
        services__in=verified_services,
    )
    if query:
        matching_services = verified_services.filter(
            Q(name__icontains=query)
            | Q(service_type__icontains=query)
            | Q(description__icontains=query)
            | Q(intended_for__icontains=query)
            | Q(city__icontains=query)
            | Q(languages__icontains=query)
            | Q(operating_hours__icontains=query)
        )
        organisations = organisations.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(city__icontains=query)
            | Q(address__icontains=query)
            | Q(country__name__icontains=query)
            | Q(services__in=matching_services)
        )
    organisations = organisations.distinct().order_by("name").prefetch_related(
        Prefetch("services", queryset=verified_services, to_attr="verified_services")
    )
    return render(
        request,
        "directory/support.html",
        {"organisations": organisations, "country": country, "query": query},
    )


def support_detail(request, id):
    country = _get_active_country()
    organisation = Organisation.objects.filter(
        country=country,
        id=id,
        is_verified=True,
        verification_status="verified",
        is_demo=False,
    ).first()
    if organisation is None:
        return render(request, "directory/support_not_found.html", {"id": id}, status=404)
    services = organisation.services.filter(
        country=country,
        is_verified=True,
        verification_status="verified",
        is_demo=False,
        is_active=True,
    )
    return render(request, "directory/support_detail.html", {"organisation": organisation, "services": services})
