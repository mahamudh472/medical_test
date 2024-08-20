from django.db import migrations, models

def clean_and_convert_amounts(apps, schema_editor):
    Test = apps.get_model('main', 'Test')
    for obj in Test.objects.all():
        amount_str = obj.tz_std_tariff.replace(',', '').replace(' ', '').strip()
        try:
            obj.tz_std_tariff = int(amount_str)
            obj.save()
        except ValueError:
            print(f"Skipping invalid amount: {obj.tz_std_tariff}")

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_service_other_time'),  # Replace with your last migration file
    ]

    operations = [
        migrations.RunPython(clean_and_convert_amounts),
        migrations.AlterField(
            model_name='test',
            name='tz_std_tariff',
            field=models.IntegerField(),
        ),
    ]
