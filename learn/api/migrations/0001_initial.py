# Generated by Django 5.2.1 on 2025-05-12 05:22

import django.db.models.deletion
import mptt.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.coursecategory')),
            ],
            options={
                'verbose_name': 'Catégorie de cours',
                'verbose_name_plural': 'Catégories de cours',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100, verbose_name='Nome Complet')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Biographie')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name': 'Formateur',
                'verbose_name_plural': 'Frmateurs',
                'ordering': ['full_name'],
                'indexes': [models.Index(fields=['full_name'], name='api_instruc_full_na_f6de1d_idx')],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix')),
                ('level', models.CharField(choices=[('beginner', 'Débutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancé')], default='beginner', max_length=20, verbose_name='Niveau')),
                ('language', models.CharField(max_length=50, verbose_name='Langue')),
                ('duration', models.PositiveBigIntegerField(verbose_name='Durée')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='api.coursecategory', verbose_name='Catégorie')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='api.instructor', verbose_name='Formateur')),
            ],
            options={
                'verbose_name': 'Cours',
                'verbose_name_plural': 'Cours',
                'ordering': ['-created_at'],
                'permissions': [('can_publish_course', 'Can publish course')],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100, verbose_name='Nom Complet')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('enrolled_courses', models.ManyToManyField(related_name='students', to='api.course', verbose_name='Cours')),
            ],
            options={
                'verbose_name': 'Etudiant',
                'verbose_name_plural': 'Etudiants',
                'ordering': ['full_name'],
            },
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['title'], name='api_course_title_050021_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['-created_at'], name='api_course_created_b1ccc3_idx'),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('title', 'instructor'), name='unique_course_per_instructor'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['full_name'], name='api_student_full_na_abfd76_idx'),
        ),
    ]
