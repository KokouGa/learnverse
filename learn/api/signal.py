from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Course

@receiver(post_save, sender=Student)
def auto_enroll_default_course(sender, instance, created, **kwargs):
    if created:
        default_course = Course.objects.filter(title__icontains="introduction").first()
        if default_course:
            instance.enrolled_courses.add(default_course)