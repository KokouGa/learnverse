import uuid
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy  as _
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
# Create your models here.




class Instructor(models.Model):
    """
    Model representing an instructor.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, verbose_name=_("Nome Complet"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    bio = models.TextField(verbose_name=_("Biographie"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    slug = models.SlugField(unique=True, blank=True)


    class Meta:
        verbose_name = _("Formateur")
        verbose_name_plural = _("Formateurs")
        ordering = ['full_name']
        indexes = [models.Index(fields=['full_name'])]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    


class CourseCategory(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Catégorie de cours"
        verbose_name_plural = "Catégories de cours"

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Model representing a course.

    This model includes fields for the course title, description, price, duration, and instructor.
    It also includes a UUID field for unique identification and timestamps for creation and update.

    """
    LEVEL_CHOICES = [
        ('beginner', _('Débutant')),
        ('intermediate', _('Intermédiaire')),
        ('advanced', _('Avancé')),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    description = models.TextField(verbose_name=_("Description"))
    slug = models.SlugField(_('Slug'),unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix"))
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name=_("Niveau"))
    language = models.CharField(max_length=50, verbose_name=_("Langue"))
    duration = models.PositiveBigIntegerField(verbose_name=_("Durée"))
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses', verbose_name=_("Formateur"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de mise à jour"))
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses', verbose_name=_("Catégorie"))

    class Meta:
        verbose_name = _("Cours")
        verbose_name_plural = _("Cours")
        ordering = ['-created_at']
        constraints = [ models.UniqueConstraint(fields=['title', 'instructor'], name='unique_course_per_instructor')]
        indexes = [models.Index(fields=['title']), models.Index(fields=['-created_at'])]
        permissions = [
            ('can_publish_course', _('Can publish course'))]


    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if self.price < 0:
            raise ValidationError(_('Le prix ne peut pas être négatif.'))
        if self.duration <= 0:
            raise ValidationError(_('La durée doit être supérieure à zéro.'))
        

    @property
    def student_count(self):
        return self.students.count()
    
    @property
    def short_description(self):
        return self.description[:100] + '...'
    

class Student(models.Model):
    """
    Model representing a student.

    This model includes fields for the student's name, email, and the courses they are enrolled in.
    It also includes a UUID field for unique identification and timestamps for creation and update.

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, verbose_name=_("Nom Complet"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    enrolled_courses = models.ManyToManyField(Course, related_name='students', verbose_name=_("Cours"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))

    class Meta:
        verbose_name = _("Etudiant")
        verbose_name_plural = _("Etudiants")
        ordering = ['full_name']
        indexes = [models.Index(fields=['full_name'])]


    def __str__(self):
        return self.full_name



