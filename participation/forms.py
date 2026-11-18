from django import forms

from .models import PartnershipInquiry, VolunteerInterest


class VolunteerInterestForm(forms.ModelForm):
    consent_to_contact = forms.BooleanField(
        required=True,
        label="I agree that MAAM may use my information to review this inquiry and contact me about it.",
        error_messages={"required": "Consent is required before you submit this inquiry."},
    )

    class Meta:
        model = VolunteerInterest
        fields = [
            "full_name",
            "email",
            "country",
            "role_interest",
            "availability",
            "motivation",
            "consent_to_contact",
        ]
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return value

    def clean_motivation(self):
        value = self.cleaned_data["motivation"].strip()
        if len(value) < 20:
            raise forms.ValidationError("Please provide a little more detail about your interest so we can review it properly.")
        return value


class PartnershipInquiryForm(forms.ModelForm):
    consent_to_contact = forms.BooleanField(
        required=True,
        label="I agree that MAAM may use my information to review this inquiry and contact me about it.",
        error_messages={"required": "Consent is required before you submit this inquiry."},
    )

    class Meta:
        model = PartnershipInquiry
        fields = [
            "organisation_name",
            "contact_name",
            "email",
            "country",
            "partnership_type",
            "message",
            "consent_to_contact",
        ]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_message(self):
        value = self.cleaned_data["message"].strip()
        if len(value) < 20:
            raise forms.ValidationError("Please share a short summary of your partnership idea.")
        return value
