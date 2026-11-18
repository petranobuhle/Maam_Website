# Database schema

## Content

- `Country`, `Language`: country/language settings
- `Topic`, `Article`, `ArticleTranslation`: education content, editorial status and optional source/image metadata
- `AudioResource`, `MediaItem`: approved audio and video/documentary/podcast metadata, including transcripts and captions links
- `LibraryResource`: categorized downloads or external resources with source information
- `CommunityStory`: curated community stories with anonymity and consent fields; publication is blocked unless consent is confirmed and the item is not demonstration content
- `Campaign`, `CampaignResource`: campaign information and campaign materials
- `Organisation`, `SupportService`: directory entries with verification status, official-source URL and demo flags

## Surveys and participation

- `Survey`, `SurveyQuestion`, `SurveyResponse`, `SurveyAnswer`: versioned survey records and submissions
- `VolunteerInterest`, `PartnershipInquiry`: contact details supplied voluntarily for follow-up
- `UserProfile`: staff/user profile metadata

## Publication safeguards

- Public directory queries require both the service and its organisation to be active, non-demo, verified and marked with `verification_status=verified`.
- Existing sample directory entries are retained but migrated to pending/unverified/inactive.
- Seed articles, translations, audio and campaign are retained and explicitly marked as demonstration or draft content.
- Public survey insights use only preset single-choice answers. Written responses are excluded. Results below five are withheld; if any category is below five, that question's full distribution is withheld to prevent inference.

The current SQLite database remains the local development database. The production PostgreSQL driver must be installed when configuring PostgreSQL.
