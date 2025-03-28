from rest_framework import serializers
from .models import Question,Choice,SubjectCategory,Category0,Category1,Questions_file,UserQuizResult,UserResponse,Leaderboard


class Category0Serializer(serializers.ModelSerializer):
    class Meta:
        model=Category0
        fields=['name']


class Category1Serializer(serializers.ModelSerializer):
    class Meta:
        model=Category1
        fields=['name' ]        

class SubjectCategorySerializer(serializers.ModelSerializer):
    questions_file_title = serializers.CharField(source='questions_file.title', read_only=True)
    class Meta:
        model=SubjectCategory
        fields=['name','questions_file_title']  ##here only taking the specific questions_file title even without declaring it in serializer        


class Questions_fileSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Questions_file
        fields=['title','category0','category1','created_at']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields='__all__'        

class QuestionSerializer(serializers.ModelSerializer):
 questions_file_title = serializers.CharField(source='questions_file.title', read_only=True)    
 subject_category_name = serializers.CharField(source='subject_category.name', read_only=True)
#  choices=ChoiceSerializer(many=True,read_only=True)
 class Meta:
        model=Question
        # fields=['text','questions_file_title','subject_category_name','id','choices']
        fields=['text','questions_file_title','subject_category_name','id']        


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserResponse
        fields=['user','question','selected_choice','is_submitted','timestamp','is_correct']
        read_only_fields=['user','is_correct','timestamp']

    def validate(self, data):
        data['user'] = self.context['request'].user
        return data   

class UserQuizResultSerializer(serializers.ModelSerializer):
    questions_file=serializers.CharField(source='questions_file.title')

    class Meta:
        model=UserQuizResult
        fields=['questions_file','points','completed_at']
        read_only_fields=['points','completed_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.full_name',read_only=True)

    class Meta:
        model=Leaderboard
        fields=['username','total_points','last_updated']    
        read_only_fields=['username','total_points','last_updated']         