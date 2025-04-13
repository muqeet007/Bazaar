from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

def create_default_store(apps, schema_editor):
    Store = apps.get_model('stock', 'Store')
    Store.objects.create(id=1, name='Default Store', location='Unknown Location')

class Migration(migrations.Migration):
    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RunPython(create_default_store),
        migrations.AddField(
            model_name='Product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='Product',
            name='description',
            field=models.TextField(default='No Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='Product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='Product',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='Product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='Product',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stock.store'),
            preserve_default=False,
        ),
    ]