from rest_framework import serializers
from .models import Question,Choice,SubjectCategory,Category,Questions_file,UserQuizResult,UserResponse,Leaderboard,Image


class CategorySerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField() 

    class Meta:
        model=Category
        fields=['level','name','id','children',] 

    def get_children(self,obj):
        return CategorySerializer(obj.children.all(), many=True).data    #You need to dynamically fetch and serialize the child categories (obj.children), and this method lets you control how that happens.

class SubjectCategorySerializer(serializers.ModelSerializer):
    questions_file_title = serializers.CharField(source='questions_file.title', read_only=True)
    class Meta:
        model=SubjectCategory
        fields=['name','questions_file_title']  ##here only taking the specific questions_file title even without declaring it in serializer        


class Questions_fileSerializer(serializers.ModelSerializer): 
    category=serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())

    class Meta:
        model=Questions_file
        fields=['title','description','category','created_at']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields='__all__'        

class QuestionSerializer(serializers.ModelSerializer):
 questions_file_title = serializers.CharField(source='questions_file.title', read_only=True)    
 subject_category_name = serializers.CharField(source='subject_category.name', read_only=True)
 images=serializers.SerializerMethodField() #Add images field and if wondering how The related_name='images' allows you to access all Image objects related to a Question instance in the reverse direction (i.e., from Question to Image).

#  choices=ChoiceSerializer(many=True,read_only=True)
 class Meta:
        model=Question
        # fields=['text','questions_file_title','subject_category_name','id','choices']
        fields=['text','questions_file_title','subject_category_name','id','images']        

 def get_images(self, obj):
    images = obj.images.all()
    result = []
    for image in images:
        try:
            image_data = {
                'id': image.id,
                'image': image.image.url if image.image else None,
                'image_url': image.image_url
            }
            result.append(image_data)
        except Exception as e:
            print(f"Error processing image {image.id}: {e}")
    return result  

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