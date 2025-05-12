import csv
from django.core.management.base import BaseCommand
from api.models import Instructor, CourseCategory, Course, Student
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Load instructors, categories, courses, students and enrollments from CSV files'

    def handle(self, *args, **kwargs):
        self.stdout.write("Chargement des instructeurs...")
        with open('data/instructors.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Instructor.objects.get_or_create(
                    email=row['email'],
                    defaults={
                        'full_name': row['full_name'],
                        'bio': row['bio'],
                    }
                )

        self.stdout.write("Chargement des catégories...")
        categories = {}
        with open('data/categories.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parent = categories.get(row['parent']) if row['parent'] else None
                category, created = CourseCategory.objects.get_or_create(
                    slug=row['slug'],
                    defaults={'name': row['name'], 'parent': parent}
                )
                categories[row['slug']] = category

        self.stdout.write("Chargement des cours...")
        with open('data/courses.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                instructor = Instructor.objects.get(email=row['instructor_email'])
                category = categories.get(row['category_slug'])
                Course.objects.get_or_create(
                    title=row['title'],
                    instructor=instructor,
                    defaults={
                        'description': row['description'],
                        'price': row['price'],
                        'level': row['level'],
                        'language': row['language'],
                        'duration': row['duration'],
                        'category': category
                    }
                )

        self.stdout.write("Chargement des étudiants...")
        with open('data/students.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Student.objects.get_or_create(
                    email=row['email'],
                    defaults={'full_name': row['full_name']}
                )

        self.stdout.write("Inscription des étudiants aux cours...")
        with open('data/enrollments.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    student = Student.objects.get(email=row['student_email'])
                    course = Course.objects.get(title=row['course_title'])
                    student.enrolled_courses.add(course)
                except (Student.DoesNotExist, Course.DoesNotExist) as e:
                    self.stdout.write(f"Erreur d'inscription : {e}")

        self.stdout.write(self.style.SUCCESS('✅ Données chargées avec succès !'))
