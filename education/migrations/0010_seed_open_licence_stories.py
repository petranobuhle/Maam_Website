"""Seed open-licence stories (republished with credit) and link-only Zimbabwean stories.

The two republished stories are CC BY 4.0. Their text was copied by script from the
publisher's full text, not retyped. External stories store no body text or photographs.
"""
import datetime

from django.db import migrations

COUNTRIES = [
    {"code": "ZA", "name": "South Africa", "official_name": "Republic of South Africa", "region": "Southern Africa"},
    {"code": "UG", "name": "Uganda", "official_name": "Republic of Uganda", "region": "East Africa"},
]

STORIES = [{'story_type': 'republished',
  'slug': 'my-bipolar-odyssey',
  'title': 'My bipolar odyssey',
  'original_title': 'Lived experience narrative: My bipolar odyssey',
  'excerpt': 'A medical doctor writes about living with bipolar disorder: the religious, cultural and social '
             'stigma she met, the self-stigma she calls “the uncommitted sin”, and how psycho-education and '
             'a supportive psychiatrist changed her care.',
  'body': 'I am a doctor. I am also a patient who has been navigating bipolar disorder for twice the '
          'lifespan of my medical career. It may seem that I am stating this with natural ease, but it '
          'certainly has not been a smooth arrival at this destination because of the stigma attached to my '
          'mental illness.\n'
          '\n'
          'It is my firm belief that the best person to tell the story of a mental illness is the person who '
          'is living with it. Sharing this bold thought feels empowering and liberating to me. I hope it '
          'will help another person who knows the difficulties that come with a life-journey alongside '
          'bipolar disorder. Having bipolar disorder in my life presented various forms of stigma. In a '
          'religious context, I was dismissed as ‘demon-possessed’ because of the mania with associated '
          'psychosis. From a cultural perspective, I was described as ‘bewitched’ because of the ‘curse of '
          'madness’ that had befallen me. In social settings, I was sometimes avoided by others, as though '
          'my strange behaviour was perhaps contagious. These stigmatising behaviours from others left me '
          'ashamed, isolated and confused, especially during my younger years.\n'
          '\n'
          'But, the worst form of stigma I have encountered was self-stigma: my own denial of my mental '
          'illness. My experience of self-stigma felt like a dark cloud that followed me everywhere. I '
          'describe it as the uncommitted sin. Sin is something that is frowned upon and often evokes shame '
          'in someone who is deemed guilty of it. Living with mental illness is not a choice that one '
          'pursues, hence it is uncommitted.\n'
          '\n'
          'It was external stigma that taught me to self-stigmatise by denying my mental illness. The lack '
          'of insight and associated shame took me along a tumultuous journey of multiple relapses and '
          'several admissions to psychiatric facilities.\n'
          '\n'
          'Unfortunately, I believe that the quality of care that I received was a contributor to my '
          'recurrent relapses. I experienced the approach of mental healthcare providers to be paternalistic '
          'and punitive. I resented this and the resentment was deepened by the frustration of caregivers '
          'and loved ones that I encountered who claimed that I deliberately refused treatment. They failed '
          'to probe and interrogate my reasons for non-adherence. A lot of my defiance was because of a lack '
          'of understanding. I lacked insight about my diagnosis and this impaired my judgement. I did not '
          'understand my illness and therefore could not accept it.\n'
          '\n'
          'Psycho-education brought an important paradigm shift to my life. I finally met my current '
          'psychiatrist who was a perfect fit for me, and remains so. They advocated for my holistic mental '
          'well-being. This approach turned my life around positively. My prognosis improved because of '
          'their empathetic and comprehensive intervention. One of the greatest gifts that I gained with my '
          'psychiatrist’s support was empowerment through self-advocacy. Now I feel as if I am a part of my '
          'management team because I have agency and a voice regarding my well-being interventions. I feel '
          'that my voice matters and that my insights are embraced and valued. I have the utmost respect for '
          'the multidisciplinary team management approach because its application has granted me quality of '
          'life.\n'
          '\n'
          'It took me 16 years to make peace and accept my diagnosis. I can confidently say that I am not '
          'suffering from bipolar disorder. I am thriving despite it.',
  'pull_quote': 'I am not suffering from bipolar disorder. I am thriving despite it.',
  'content_note': 'This story mentions mania, psychosis, stigma, refusing treatment and admissions to '
                  'psychiatric facilities.',
  'author_display': 'Samukelisiwe J. Ngcobo',
  'is_anonymous': False,
  'author_affiliation': 'Vocal Mentality, Johannesburg, South Africa',
  'author_note': 'Samukelisiwe J. Ngcobo is a medical doctor, author and international speaker who is a '
                 'mental health activist and founder of Vocal Mentality. Her personal platforms '
                 'www.vocalmentality.com and Sisters For Mental Health have a focus of destigmatising mental '
                 'illness and educating society about mental health.',
  'country': 'ZA',
  'source_name': 'South African Journal of Psychiatry (AOSIS)',
  'source_url': 'https://sajp.org.za/index.php/sajp/article/view/2339',
  'doi_url': 'https://doi.org/10.4102/sajpsychiatry.v30i0.2339',
  'published_on': '2024-07-19',
  'licence_name': 'CC BY 4.0',
  'licence_url': 'https://creativecommons.org/licenses/by/4.0/',
  'copyright_notice': '© 2024. The Author. Licensee: AOSIS.',
  'attribution_text': '“Lived experience narrative: My bipolar odyssey” by Samukelisiwe J. Ngcobo, first '
                      'published in the South African Journal of Psychiatry, Vol. 30 (2024), a2339, on 19 '
                      'July 2024. © 2024. The Author. Licensee: AOSIS. Licensed under the Creative Commons '
                      'Attribution 4.0 International licence (CC BY 4.0).',
  'changes_note': 'The article text and author biography are reproduced in full, without edits. MAAM '
                  "shortened the display title by leaving out the journal's section label (“Lived experience "
                  'narrative:”), and added the page layout, a summary, a content note and a pull quote taken '
                  'word-for-word from the text.',
  'permission_notes': "Licence checked on the publisher's page on 18 November 2026. Article page footer: “© "
                      '2024 Samukelisiwe J. Ngcobo | This work is licensed under Other”, linking to '
                      'https://creativecommons.org/licenses/by/4.0/. Article XML: “© 2024. The Author” and '
                      '“Licensee: AOSIS. This work is licensed under the Creative Commons Attribution '
                      'License.” Journal policy: all articles CC BY 4.0 unless otherwise stated. No '
                      'photographs in the article. Do not use a photograph of the author without separate '
                      'permission.',
  'is_featured': True,
  'display_order': 10},
 {'story_type': 'republished',
  'slug': 'life-beyond-diagnosis',
  'title': 'Life beyond diagnosis: My journey of hope',
  'original_title': 'Life beyond diagnosis: My journey of hope',
  'excerpt': 'Eddie Nkurunungi describes his first experiences of mental illness in Uganda, seven years in a '
             'secure hospital in London, diagnoses that kept changing, and how the service user movement and '
             'peer support gave his life meaning and purpose.',
  'body': 'My name is Eddie Nkurunungi. When I was born, my mother asked the sex, and they said, ‘it is a '
          'boy’. So, she said, ‘good news’: Nkuru is news, nungi is good. So, I became Nkurunungi, the '
          'gospel.\n'
          '\n'
          'My family comes from Southwestern Uganda, Ahamunyinya Village: a place where acacia trees are '
          'found. My dad was a headteacher but moved to Kampala to work for Save the Children, then the '
          'United Nations (UN): so, I was raised as a city kid in a block of flats, speaking many languages, '
          'Luganda, Swahili, Arabic, Nubian and our native Rukiga.\n'
          '\n'
          'I enjoyed school, but was a bit naughty, in trouble for speaking in class, and speaking our '
          'native language vernacular, which was punishable: you are meant to speak English only at school. '
          'They would read out names of ‘vernacular speakers’ at assembly, and you would be smacked.\n'
          '\n'
          'My mother sold used clothes from Europe and had a grocery shop. She was welcoming but had a '
          'problem with alcohol. This brought conflict with my dad, and they would fight. They separated '
          'when I was five, and we moved to Mbarara with my mother.\n'
          '\n'
          'We came back to Kampala when I was eight, and I was popular at school and fast at making friends. '
          'When I joined secondary school, I was in rhyme with the establishment and made head prefect.\n'
          '\n'
          'I experienced the first signs of mental illness at tertiary college while running for election. '
          'There was pressure to fundraise to grease the hands of voters, and there was witch-hunting and '
          'backstabbing from my opponents, looking for negative things to tarnish my name. The pressure '
          'strained me.\n'
          '\n'
          'I did not feel safe. I left my roommates, moved in with my girlfriend, then my uncle, where I '
          'barricaded myself with furniture at the door. Neighbours broke the door and manhandled me to the '
          'police, where a psychiatric clinical officer (PCO) tried to talk to me but realised I was violent '
          'and sedated me.\n'
          '\n'
          'I woke naked on a concrete floor, with no toilet or water. Attendants would bring food and close '
          'the door again. I tried to get out, but there was no window; I tried to call for help, but nobody '
          'would come. After a few days, my parents visited, and I got some fresh air. I was in uniform '
          'shorts without a shirt, saw other people in uniform and realised that I was locked up in '
          'hospital. I did not even know that place existed.\n'
          '\n'
          'After a few days, I saw a psychiatrist. I was disoriented and could not comprehend. They forced '
          'me with medication, sedatives and antipsychotics. I asked what they were treating, but nobody '
          'would answer.\n'
          '\n'
          'I did not see the need to stay in the hospital and helped myself out: there was no serious fence, '
          'and I just left. I walked through villages, got money for a taxi, but they said, ‘go away, go '
          'back’ because of the uniform shorts I was wearing, they were stigmatising me. I guessed my '
          'college was in the west, so I followed the sunset. At college, friends saw me in a sorry state, '
          'disoriented and out of focus, in uniform shorts and with wounds all over my body: they were '
          'supportive and kind and got me to my parents.\n'
          '\n'
          'I received treatment from the PCO that first saw me. Later on, I understood that they were '
          'treating bipolar disorder but at the time, they just said ‘you’re mulalu’ which means ‘mad’. The '
          'treatment was carbamazepine that would make me shake like a leaf, dribble and doze off. '
          'Eventually, the fear, paranoia, restlessness and overtalking receded, and I returned to college '
          'to complete my studies.\n'
          '\n'
          'In 1999, my mother died, which devastated me and left a vacuum in my life. I decided to join my '
          'siblings in London and stayed with my sister in her one-bedroom flat.\n'
          '\n'
          'In the United Kingdom (UK), I faced a cultural clash: life was fast, and I had to work hard to '
          'make ends meet: cleaning toilets from 06:00 then working in a restaurant until 23:00. Within 2 '
          'weeks, I had broken down mentally.\n'
          '\n'
          'I was not sleeping and barricaded myself in the house, paranoid that police were looking for me. '
          'My sister called the police, who broke the door but let me go, so I started to look for the '
          'Ugandan High Commission to help me get home.\n'
          '\n'
          'I walked the whole night, but everything was too fast. I was racing with cars, stripped naked, '
          'jumped over a fence, and I was brought down by the police. They asked my name: I did not know '
          'whether to tell them a pseudonym or my actual name. They took me to a psychiatric hospital. They '
          'gave me carbamazepine and told me it was bipolar. I was discharged, but they did not give me a '
          'follow-up plan, because they thought that I was going back to Uganda.\n'
          '\n'
          'I found a new job under a pseudonym, but had a constant fear that the police would find out I was '
          'working illegally. This increased to paranoia: I thought the police were coming and assaulted my '
          'sister. I was confused, my mind was too much, and I thought of jumping off the balcony. The '
          'police arrested me and then took me to the hospital.\n'
          '\n'
          'I was taken to court and was found ‘not guilty’ by virtue of insanity: they recommended treatment '
          'in a secure setting without limit of time, under home office restrictions. I then spent the next '
          '7 years in a hospital in incarceration.\n'
          '\n'
          'My diagnosis changed to paranoid schizophrenia. I had never heard of that diagnosis and even now, '
          'I do not resonate with schizophrenia: although I experience paranoia, I do not experience '
          'hallucinations.\n'
          '\n'
          'I thought they were racist to give me this diagnosis, because the index offence was violent. I '
          'did not understand the intensity of the diagnosis; it was just some verbose words. But when you '
          'read about schizophrenia, the prognosis is poor, the chances of recovery are not there. It would '
          'mean I would never function on my own; never be able to sustain a job, have a family or raise '
          'children. I would not be responsible, just some hopeless person who cannot achieve anything.\n'
          '\n'
          'At my first tribunal, my diagnosis changed to schizoaffective disorder because of my history of '
          'bipolar. These were words that I was not familiar with, but I learned that the prognosis of '
          'schizoaffective disorder was more positive: people can recover. My treatment was reduced to a '
          'monthly injection.\n'
          '\n'
          'There was a helpful psychotherapist whom I saw for 5 years, who helped me understand the genesis '
          'of my mental disorder in my upbringing as a child.\n'
          '\n'
          'Occupational therapy was the most helpful to get routine, shopping and cooking, interacting with '
          'peers, undertaking IT training, getting paid roles, cleaning the ward and working in the '
          'canteen.\n'
          '\n'
          'As Foundation Trusts were launched, there was a requirement for service user representation, and '
          'I would meet with clinicians, who listened to our experiences of institutional settings, the care '
          'we needed, the life we wanted: that is how I started my journey with the service user movement.\n'
          '\n'
          'At my last tribunal, my diagnosis was changed back to paranoid schizophrenia-in-remission because '
          'I had no mood swings or extremes of energy during my 7 years in hospital. I then returned to '
          'Uganda in August 2007.\n'
          '\n'
          'When I left Uganda, I had a culture shock in London, but when I returned, I got an aftershock '
          'because so much had changed. My friends had moved on, were now big guys, in government, with '
          'families. I could not relate to them and saw myself as an underdog, as someone who had gone to '
          'the UK and wasted his time in a secure setting, coming back with nothing to show.\n'
          '\n'
          'I felt out of place, but in the service user movement, I found people who believed in me and '
          'accepted me for who I am. I felt comfortable and, with time, started opening up. In London, I was '
          'told, ‘don’t tell people what happened to you, don’t share your index offence, just keep it to '
          'yourself’. But now I have found peers who were outspoken and proud of their identity as service '
          'users with lived experience. Being part of Heartsounds helped me spread my wings.\n'
          '\n'
          'Joining the mental health service user movement has brought meaning and purpose. I coordinated '
          'the Butabika Recovery College and founded Peer Nation, a non-governmental organisation (NGO) of '
          'which I am the Chief Executive Officer (CEO). I have coordinated Peer Support Workers training '
          'and working all over Uganda, in the community and in refugee settlements; coordinated the Brain '
          'Gain and Using Peer Support in Developing Empowering Mental Health Services (UPSIDES) projects, '
          'secured funding from Department For International Development (UK Aid) (DFID) and/or Tropical '
          'Health and Education Trust (THET), the Storm Fund, Open Society Initiative for East Africa '
          '(OSIEA) and the Disability Rights Fund. I have met ministers, lobbied for the Mental Health Act '
          '(MHA) reform on radio and television, and travelled to Tanzania, Rwanda and South Africa to talk '
          'about service user involvement. This is the legacy I would wish to leave behind.\n'
          '\n'
          'There is more to a human being than a diagnosis. A diagnosis can be transient, a working '
          'hypothesis that could be proved right or wrong: it should never be cast in stone. It is the '
          'people and the stories behind their diagnosis and labels that matter the most.',
  'pull_quote': 'There is more to a human being than a diagnosis.',
  'content_note': 'This story describes psychosis, police involvement, forced medication and seclusion, an '
                  'assault on a family member, a brief mention of thoughts of jumping from a balcony, and '
                  'long-term detention in a secure hospital.',
  'author_display': 'Edward Nkurunungi',
  'is_anonymous': False,
  'author_affiliation': 'Department of Administration, Peer Nation, Kampala, Uganda',
  'author_note': '',
  'country': 'UG',
  'source_name': 'South African Journal of Psychiatry (AOSIS)',
  'source_url': 'https://sajp.org.za/index.php/sajp/article/view/2714',
  'doi_url': 'https://doi.org/10.4102/sajpsychiatry.v32i0.2714',
  'published_on': '2026-06-19',
  'licence_name': 'CC BY 4.0',
  'licence_url': 'https://creativecommons.org/licenses/by/4.0/',
  'copyright_notice': '© 2026. The Author. Licensee: AOSIS.',
  'attribution_text': '“Life beyond diagnosis: My journey of hope” by Edward Nkurunungi, first published in '
                      'the South African Journal of Psychiatry, Vol. 32 (2026), a2714, on 19 June 2026. © '
                      '2026. The Author. Licensee: AOSIS. Licensed under the Creative Commons Attribution '
                      '4.0 International licence (CC BY 4.0).',
  'changes_note': 'The article text is reproduced in full, without edits. MAAM added the page layout, a '
                  'summary, a content note and a pull quote taken word-for-word from the text.',
  'permission_notes': "Licence checked on the publisher's page on 18 November 2026. Full-text page: "
                      '“Copyright: © 2026. The Author. Licensee: AOSIS. This work is licensed under the '
                      'Creative Commons Attribution 4.0 International (CC BY 4.0) license '
                      '(https://creativecommons.org/licenses/by/4.0/).” No photographs in the article. Do '
                      'not use a photograph of the author without separate permission.',
  'is_featured': False,
  'display_order': 20},
 {'story_type': 'external',
  'slug': 'unicef-zimbabwe-mental-health-everyones-business',
  'title': "Mental health is everyone's business",
  'original_title': "Mental health is everyone's business",
  'excerpt': 'A young Zimbabwean social worker writes about losing her brother to suicide and how it led her '
             'to mental health advocacy with other young people.',
  'body': '',
  'pull_quote': '',
  'content_note': 'This story discusses suicide and substance use.',
  'author_display': 'Tsungirirai Lucia Paridzira',
  'is_anonymous': False,
  'author_affiliation': '',
  'author_note': '',
  'country': 'ZW',
  'source_name': 'UNICEF Zimbabwe',
  'source_url': 'https://www.unicef.org/zimbabwe/stories/mental-health-everyones-business',
  'doi_url': '',
  'published_on': '2022-12-07',
  'licence_name': '',
  'licence_url': '',
  'copyright_notice': '',
  'attribution_text': '',
  'changes_note': '',
  'permission_notes': 'Checked 18 November 2026: no open licence shown on the page. Photos credited '
                      '“UNICEFZimbabwe/2022/UNICEF”. Link only: do not copy text or photos. Ask UNICEF '
                      'Zimbabwe and the author for written permission before republishing.',
  'is_featured': False,
  'display_order': 10},
 {'story_type': 'external',
  'slug': 'inspire-the-mind-zimbabwean-youth-demystifying-mental-health',
  'title': 'Zimbabwean Youth Approach to demystifying Mental Health',
  'original_title': 'Zimbabwean Youth Approach to demystifying Mental Health',
  'excerpt': 'Tanatswa Chikaura, who was born and raised in Zimbabwe, writes about how she came to youth '
             "mental health advocacy and about the Ndinewe Foundation's community work in Harare.",
  'body': '',
  'pull_quote': '',
  'content_note': 'This article discusses suicide and substance use.',
  'author_display': 'Tanatswa Chikaura',
  'is_anonymous': False,
  'author_affiliation': '',
  'author_note': '',
  'country': 'ZW',
  'source_name': 'Inspire the Mind',
  'source_url': 'https://www.inspirethemind.org/post/zimbabwean-youth-approach-to-demystifying-mental-health',
  'doi_url': '',
  'published_on': '2023-06-12',
  'licence_name': '',
  'licence_url': '',
  'copyright_notice': '',
  'attribution_text': '',
  'changes_note': '',
  'permission_notes': 'Checked 18 November 2026: no open licence shown on the page. Photos credited “Photo '
                      'by Ndinewe Foundation”. Link only: do not copy text or photos. Ask Inspire the Mind '
                      'and the author for written permission before republishing.',
  'is_featured': False,
  'display_order': 20}]


def seed_stories(apps, schema_editor):
    Country = apps.get_model("core", "Country")
    CommunityStory = apps.get_model("education", "CommunityStory")
    for fields in COUNTRIES:
        # New countries stay inactive so they do not change other pages.
        Country.objects.get_or_create(code=fields["code"], defaults={**fields, "is_active": False})

    for story in STORIES:
        fields = dict(story)
        country = Country.objects.get(code=fields.pop("country"))
        fields["published_on"] = datetime.date.fromisoformat(fields["published_on"])
        CommunityStory.objects.get_or_create(
            slug=fields.pop("slug"),
            defaults={**fields, "country": country, "is_published": True, "is_demo": False},
        )


def remove_stories(apps, schema_editor):
    CommunityStory = apps.get_model("education", "CommunityStory")
    CommunityStory.objects.filter(slug__in=[story["slug"] for story in STORIES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_country_language_data"),
        ("education", "0009_communitystory_licensing_fields"),
    ]

    operations = [
        migrations.RunPython(seed_stories, remove_stories),
    ]
