# Privacy and safeguarding

MAAM provides mental-health awareness and advocacy information. It is not a diagnosis, counselling, treatment or emergency service.

## Data minimisation and access

- Anonymous surveys ask for consent and a broad age band, not name or contact details.
- Written survey answers may be stored for restricted staff review, but are never included in public insights.
- Public survey outputs use preset choice options only. Fewer than five responses are not published; any distribution containing a cell below five is withheld in full.
- Volunteer and partnership forms collect contact details only for follow-up. Contributors should not include health details or third-party information.
- Staff-only dashboards require authenticated staff access. Django admin access should be limited to trusted administrators.

## Stories and media

- Do not publish a personal story without informed, specific consent for the intended use.
- Anonymous attribution must be respected; remove identifying details from text and media.
- Use only images, audio and video for which MAAM has appropriate publication rights and consent.
- Provide captions or transcripts where available and useful alt text for meaningful images.

## Support directory

Only publish current entries after checking the organisation, service and contact information against an official source. Demonstration and unverified records remain hidden from public listings.

## Staff email notifications (Batch 3)

- **When:** a successful Volunteer or Partnership submission triggers one email to MAAM's own address, sent through Resend.
- **What it contains:** by design, only the form type, submission time, reference ID and an admin link. It never includes the person's name, email address or message, so submitters' personal details are not passed to Resend or stored in an email inbox.
- **Where to read submissions:** in the login-protected admin.
- **Logs:** only the reference ID and an HTTP status, never personal details or the API key.
- **Not a support service:** the email reminds staff that MAAM is not a counselling or emergency service, and to follow safeguarding guidance if a submission raises a concern.
- **Data processors:** in production, submissions are stored in Neon PostgreSQL, hosted on behalf of MAAM, and the site runs on Render. Mention these hosting providers when the privacy notice is next reviewed.

## Before public launch

Confirm privacy contact details, retention periods, hosting-provider log retention, jurisdiction-specific requirements, staff access controls, incident response and consent wording. Never use the prototype to collect urgent requests; the site is not monitored for emergencies.
