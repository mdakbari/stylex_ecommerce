# Generated by Django 4.2.4 on 2024-04-05 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('street_address', models.TextField(null=True)),
                ('country', models.CharField(default='India', max_length=30, null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('phone_number', models.BigIntegerField(null=True)),
                ('email', models.CharField(max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=50)),
                ('Comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='placeOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.CharField(max_length=50, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('shipping_charge', models.IntegerField(null=True)),
                ('total_quantity', models.IntegerField(null=True)),
                ('total_amount', models.IntegerField(null=True)),
                ('order_id', models.IntegerField(null=True)),
                ('address_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.addressmodel')),
            ],
        ),
        migrations.CreateModel(
            name='stateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='sub_placeorder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, null=True)),
                ('size', models.CharField(max_length=50, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.placeorder')),
                ('subproduct_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_app.subproduct')),
            ],
        ),
        migrations.AddField(
            model_name='placeorder',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('size', models.CharField(max_length=50, null=True)),
                ('color', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.subproduct')),
                ('uname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
            options={
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.AddField(
            model_name='addressmodel',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.statemodel'),
        ),
        migrations.AddField(
            model_name='addressmodel',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
