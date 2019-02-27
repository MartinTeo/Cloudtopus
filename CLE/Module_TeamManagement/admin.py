from django.contrib import admin
from Module_TeamManagement.models import *

class StudentAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('email', 'username', 'firstname', 'lastname', 'telegram_username','loginCounts')
    # add filtering by date
    #list_filter = ('date',)
    # add search field 
    search_fields = ['email', 'firstname']

class CourseAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('course_title', 'course_name', 'course_description')

class CourseSectionAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('course_section_id', 'course_name', 'section_number')
    def course_name(self,obj):
        return obj.course.course_title
class FacultyAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
   
    list_display = ('email', 'username', 'firstname','lastname', 'all_course_sections', 'awscredential' )
    
    def all_course_sections(self, obj):
        return "\n".join([p.to_string for p in obj.course_section.all()])

class SchoolTermAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('school_term_id', 'term', 'financial_year', 'start_date','end_date')
    list_filter = ('term',)

class ClassAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('course_section_id','school_term_id', 'student_id', 'team_number', 'awscredential')
    list_filter = ('course_section_id','school_term_id','team_number' )

    def course_section_id(self,obj):
        return obj.course_section.course_section_id

    def student_id(self,obj):
        return obj.student.email

    def school_term_id(self,obj):
        return obj.school_term.school_term_id

class TelegramAdmin(admin.ModelAdmin):
    list_display= ('name', 'type', 'members', 'link')

admin.site.register(Student, StudentAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Course_Section, CourseSectionAdmin)
admin.site.register(Faculty,FacultyAdmin)
#admin.site.register(Cloud_Learning_Tools)
admin.site.register(School_Term,SchoolTermAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Telegram_Chats,TelegramAdmin)

# Register your models here.
