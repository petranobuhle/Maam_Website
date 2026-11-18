# Story permissions and licence record

Last checked: 18 November 2026. Check again before public launch, and whenever a story is added.

The Stories page ("Beyond the Silence: Real Voices. Real Experiences.") has three kinds of story. You choose the kind with `story_type` in the admin.

| Type | What MAAM may show | Rule |
|---|---|---|
| Community | Full text | Only with the storyteller's informed consent (`consent_confirmed`). |
| Republished | Full text | Only under an open licence or written permission, with full credit. |
| External | Title, author, publisher, date and a short summary written by MAAM | A link to the original. No copied text and no photographs. |

## Republished under CC BY 4.0

Both stories come from the *South African Journal of Psychiatry* (publisher AOSIS). The journal says: "All articles published in this journal are licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license, unless otherwise stated."

**What CC BY 4.0 requires** (https://creativecommons.org/licenses/by/4.0/):

1. Credit the author and the source.
2. Keep the copyright notice.
3. Link to the licence.
4. Say whether you made changes.
5. Do not suggest that the author or publisher endorses MAAM.

The story page shows all five.

### 1. My bipolar odyssey: Samukelisiwe J. Ngcobo

- **Original title:** "Lived experience narrative: My bipolar odyssey"
- **Published in:** S Afr J Psychiat. 2024;30(0), a2339. Published 19 July 2024.
- **DOI:** https://doi.org/10.4102/sajpsychiatry.v30i0.2339
- **Source:** https://sajp.org.za/index.php/sajp/article/view/2339
- **Affiliation as printed:** Vocal Mentality, Johannesburg, South Africa
- **Licence wording:**
  - In the article XML: "© 2024. The Author" and "Licensee: AOSIS. This work is licensed under the Creative Commons Attribution License."
  - In the page footer: "© 2024 Samukelisiwe J. Ngcobo | This work is licensed under Other", which links to CC BY 4.0.
- **Changes by MAAM:**
  - The text and author biography are unedited.
  - The display title leaves out "Lived experience narrative:".
  - MAAM added the layout, a summary, a content note and a pull quote copied word-for-word.
- **Photographs:** none in the article. A photo of the author needs separate permission.

### 2. Life beyond diagnosis: My journey of hope: Edward Nkurunungi

- **Published in:** S Afr J Psychiat. 2026;32(0), a2714. Published 19 June 2026.
- **DOI:** https://doi.org/10.4102/sajpsychiatry.v32i0.2714
- **Source:** https://sajp.org.za/index.php/sajp/article/view/2714
- **Affiliation as printed:** Department of Administration, Peer Nation, Kampala, Uganda
- **Licence wording:** "Copyright: © 2026. The Author. Licensee: AOSIS. This work is licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license."
- **Changes by MAAM:**
  - The text is unedited.
  - MAAM added the layout, a summary, a content note and a pull quote copied word-for-word.
- **Photographs:** none in the article. A photo of the author needs separate permission.

## External links only: permission needed before republishing

| Story | Author | Publisher and date | Licence found | Photos |
|---|---|---|---|---|
| [Mental health is everyone's business](https://www.unicef.org/zimbabwe/stories/mental-health-everyones-business) | Tsungirirai Lucia Paridzira | UNICEF Zimbabwe, 7 December 2022 | None shown | Credited "UNICEFZimbabwe/2022/UNICEF". Do not copy. |
| [Zimbabwean Youth Approach to demystifying Mental Health](https://www.inspirethemind.org/post/zimbabwean-youth-approach-to-demystifying-mental-health) | Tanatswa Chikaura | Inspire the Mind, 12 June 2023 | None shown | Credited "Photo by Ndinewe Foundation". Do not copy. |

To republish either story, get written permission from both the publisher and the author for the text and for any photos. Then:

1. Change the story to "Republished".
2. Add the text and credits.
3. Record the permission in `permission_notes`.

## Resource library images (checked 18 November 2026)

The images are stored in `static/images/resources/`. The credit and licence for each one are shown on its card and saved in the admin.

### Friendship Bench publications

- **File:** `friendship-bench-harare-costa-juta.jpg`
- **What it shows:** a Friendship Bench grandmother and a client in a problem-solving therapy session in Harare.
- **Photographer:** Costa Juta, 2022.
- **Licence:** CC BY-SA 4.0. Wikimedia Commons confirmed the photographer's permission (VRT ticket 2022102110144325).
- **Source:** https://commons.wikimedia.org/wiki/File:Friendship-Bench-Zimbabwe.jpg
- **Edits:** none. It is Wikimedia's 1280px copy. If MAAM edits the image, the edited version must also be shared under CC BY-SA 4.0.

### Doing What Matters in Times of Stress (WHO)

- **File:** `who-doing-what-matters-cover.jpg`
- **What it shows:** the official front cover of the guide.
- **Licence:** the publication is CC BY-NC-SA 3.0 IGO, which allows non-commercial use with credit.
- **WHO logo:** WHO's licence does not allow use of the WHO logo. The card shows only the top of the cover, so the logo is not visible.
- **Condition:** this licence applies only while MAAM's use stays non-commercial.

### No image: copyright reserved, permission needed

| Resource | Rights holder | Who to ask |
|---|---|---|
| Mental health of adolescents | © WHO | WHO permissions |
| Mental health and well-being | © UNICEF | UNICEF |
| The State of the World's Children 2021 | © UNICEF | UNICEF permissions office, nyhqdoc.permit@unicef.org |

## Site images (checked 18 November 2026)

### About page: `static/images/about-highfield-harare-dawn.jpg`

- **Source:** "Dawn in Highfield Harare 2" by **Achitate**, from Wikimedia Commons (Wiki Loves Africa 2015). https://commons.wikimedia.org/wiki/File:Dawn_in_Highfield_Harare_2.jpg
- **Licence:** CC BY-SA 4.0.
- **How it was confirmed:** the original file was byte-for-byte identical to the Commons file (SHA-1 `ea248b3c…d23e`).
- **Changes:** resized from 3888×2592 to 1600×1067 and re-compressed. The credit says "(resized)". If the image is adapted further, the adapted version must also be shared under CC BY-SA 4.0.
- **Credit:** shown under the photo on the About page.

### Homepage: `static/images/homepage-maam-hero.jpg`

- **Source:** the original PNG carried Content Credentials (C2PA) metadata. It records creation by **ChatGPT (OpenAI gpt-image)** on 17 November 2026, with source type "trainedAlgorithmicMedia", meaning AI-generated.
- **Rights:** OpenAI's terms assign output rights to the user who created it, so no third-party credit is required. **The MAAM owner must confirm** they created it with their own account.
- **Metadata:** compression removed the C2PA metadata. The original, with its credentials, is kept in `MAAM_backup_2026-11-18_batch2/original-images/`.
- **Disclosure (not yet decided):** the site promises elsewhere not to invent people or photographs. Consider a caption such as "Illustration created with AI".

## Adding photographs or video

- Use only photographs you own, have written permission for, or that carry an open licence.
- Always fill in `image_alt` and `image_credit`. The admin will not publish a story without them.
- Embed a video only when the owner allows embedding, and credit it in `video_credit`.
- Do not use photographs of real people without their consent.
