# Generated by Django 4.0.2 on 2022-04-10 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_activeplayer_player_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeplayer',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='LaserTagMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message_isnew', models.BooleanField(default=True)),
                ('player1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player1_reference', to='home.activeplayer')),
                ('player2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player2_reference', to='home.activeplayer')),
            ],
        ),
    ]
