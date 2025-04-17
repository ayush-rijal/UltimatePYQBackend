from django.contrib import admin
from .models import Category, Questions_file, Question, Choice, SubjectCategory,UserResponse,UserQuizResult,Leaderboard,Image

from django.utils.html import format_html


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('question', 'display_image', 'image_url')
    readonly_fields = ('display_image_field',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    display_image.short_description = "Image Preview"

    def display_image_field(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" height="300" />', obj.image.url)
        return "No Image"
    display_image_field.short_description = "Image"





class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'parent','level')
    search_fields=('name',)   
   

class Questions_fileAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','created_at')    
    search_fields = ('title', 'category__name')
    list_filter = ( 'created_at','category')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category','questions_file')}),
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

# class QuizResultAdmin(admin.ModelAdmin):
#     list_display=('user','questions_file','question','selected_choice','is_correct', 'points' , 'attempted_at')
#     search_fields = ('question__text', 'questions_file','user')

class UserResponseAdmin(admin.ModelAdmin):
    list_display=('user','question','selected_choice','is_correct','timestamp')
    search_fields=('question__text','id','user')

class UserQuizResultAdmin(admin.ModelAdmin):
    list_display=('user','questions_file','points','completed_at')
    search_fields=('user','questions_file')

class LeaderboardAdmin(admin.ModelAdmin):
    list_display=('user','total_points','last_updated')
    search_fields=('user','total_points')




admin.site.register(Category,CategoryAdmin)
admin.site.register(Questions_file, Questions_fileAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(SubjectCategory, SubjectCategoryAdmin)
# admin.site.register(QuizResult, QuizResultAdmin)

admin.site.register(UserResponse,UserResponseAdmin)
admin.site.register(UserQuizResult,UserQuizResultAdmin)
admin.site.register(Leaderboard,LeaderboardAdmin)
