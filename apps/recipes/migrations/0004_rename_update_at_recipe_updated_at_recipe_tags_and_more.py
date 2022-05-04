# Generated by Django 4.0.4 on 2022-05-04 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_remove_tag_content_type_remove_tag_object_id'),
        ('recipes', '0003_alter_recipe_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, default='', to='tag.tag'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]