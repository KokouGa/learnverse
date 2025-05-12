from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.translation import gettext_lazy as _
from .models import Instructor, CourseCategory, Course, Student


admin.site.site_header = "Administration des Cours"
admin.site.site_title = "Admin portal des Cours"
admin.site.index_title = "Tableau de bord de l'administration des cours"



# -------------------------------
# Instructor
# -------------------------------
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at")
    search_fields = ("full_name", "email")
    prepopulated_fields = {"slug": ("full_name",)}
    ordering = ("full_name",)
    list_filter = ("created_at",)
    date_hierarchy = "created_at"


# -------------------------------
# CourseCategory (hiérarchie MPTT)
# -------------------------------
@admin.register(CourseCategory)
class CourseCategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ("tree_actions", "indented_title", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("tree_id", "lft")


# -------------------------------
# Course
# -------------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "instructor", "level",
        "duration", "price", "language", "created_at"
    )
    list_filter = ("category", "instructor", "level", "language", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category", "instructor")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "student_count", "short_description")

    fieldsets = (
        (_("Informations principales"), {
            "fields": ("title", "slug", "description", "short_description", "category", "instructor")
        }),
        (_("Détails"), {
            "fields": ("price", "level", "language", "duration")
        }),
        (_("Dates & publication"), {
            "fields": ("created_at", "updated_at")
        }),
    )


# -------------------------------
# Student
# -------------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at")
    search_fields = ("full_name", "email")
    filter_horizontal = ("enrolled_courses",)
    ordering = ("full_name",)
    date_hierarchy = "created_at"
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    
