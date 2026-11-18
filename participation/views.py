from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import PartnershipInquiryForm, VolunteerInterestForm
from .notifications import notify_new_submission


def get_involved(request):
    volunteer_form = VolunteerInterestForm()
    partnership_form = PartnershipInquiryForm()

    if request.method == "POST":
        if "volunteer_submit" in request.POST:
            volunteer_form = VolunteerInterestForm(request.POST)
            if volunteer_form.is_valid():
                submission = volunteer_form.save()
                notify_new_submission(submission, request)
                messages.success(request, "Your volunteer interest has been received.")
                return redirect("get-involved")
        elif "partnership_submit" in request.POST:
            partnership_form = PartnershipInquiryForm(request.POST)
            if partnership_form.is_valid():
                submission = partnership_form.save()
                notify_new_submission(submission, request)
                messages.success(request, "Your partnership inquiry has been received.")
                return redirect("get-involved")
        else:
            messages.error(request, "Please choose a form before submitting.")

    return render(
        request,
        "participation/get_involved.html",
        {"volunteer_form": volunteer_form, "partnership_form": partnership_form},
    )
