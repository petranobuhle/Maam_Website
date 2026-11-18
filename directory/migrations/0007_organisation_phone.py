from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0006_seed_verified_zimbabwe_listings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="phone",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
