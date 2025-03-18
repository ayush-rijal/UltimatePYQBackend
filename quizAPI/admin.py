from django.contrib import admin
from .models import Category0, Category1, Questions_file, Question, Choice, SubjectCategory


class Category0Admin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class Category1Admin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)    

class Questions_fileAdmin(admin.ModelAdmin):
    list_display = ('title', 'category0', 'category1','created_at')    
    search_fields = ('title', 'category0__name')
    list_filter = ('category0', 'created_at')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category0', 'category1','questions_file')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')

class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'questions_file')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject_category')
    search_fields = ('text',)
    list_filter = ('subject_category',)        

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question__text', 'text')


admin.site.register(Category0,Category0Admin)
admin.site.register(Category1,Category1Admin)
admin.site.register(Questions_file, Questions_fileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(SubjectCategory, SubjectCategoryAdmin)