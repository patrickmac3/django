# Generated by Django 5.0.1 on 2024-03-19 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_rename_propertyimage_propertyprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='condounit',
            name='image',
            field=models.ImageField(default='condoUnit_images/defaultCondoUnit.jpg', upload_to='condoUnit_images'),
        ),
        migrations.AddField(
            model_name='parkingunit',
            name='image',
            field=models.ImageField(default='parkingUnit_images/defaultParkingUnit.jpg', upload_to='parkingUnit_images'),
        ),
        migrations.AddField(
            model_name='storageunit',
            name='image',
            field=models.ImageField(default='storageUnit_images/defaultStorageUnit.jpg', upload_to='storageUnit_images'),
        ),
    ]