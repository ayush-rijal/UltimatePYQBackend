from django.db import models
import pandas as pd
from django.contrib.auth import get_user_model
import os
from django.core.files import File

class Category(models.Model):
    name=models.CharField(max_length=15,unique=True)
    parent=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='children')
    level=models.PositiveBigIntegerField(default=0)
    
    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name

    '''
    Normally, save() just writes the object to the database. Here, you’re adding logic to update level before that happens.
    '''
    def save(self,*args,**kwargs):
        if self.parent:
            self.level=self.parent.level+1
        else:
            self.level=0
        super().save(*args,**kwargs)   

class Image(models.Model):
    image = models.ImageField(upload_to='quiz/images/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='images', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.question.text[:50]}"


class Questions_file(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    category=models.ForeignKey(Category,related_name='questions_files',on_delete=models.CASCADE,null=True) #Multiple Categories
    questions_file=models.FileField(upload_to='quiz/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True),
    id=models.AutoField(primary_key=True)

    class Meta:
        verbose_name_plural='questions_file'

    def __str__(self):
        return self.title 
      
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.questions_file:
            self.import_questions_from_excel()

    def import_questions_from_excel(self):
        try:
            df=pd.read_excel(self.questions_file.path)   
            df.columns=df.columns.str.strip()

            # Get the directory of the Excel file to resolve relative image paths
            # excel_dir = os.path.dirname(self.questions_file.path) 
            for index, row in df.iterrows():
                try:
                    question_text=str(row['Question']).strip()
                    print(f"Processing Question: {question_text}")

                    choices={
                        'A':str(row['A']).strip(),
                        'B':str(row['B']).strip(),
                        'C':str(row['C']).strip(),
                        'D':str(row['D']).strip(),
                    }
                    correct_answer= row['Answer'].strip() ##either A or B or C or D is stored in correct_answer
                    subject_category=str(row['SubjectCategory']).strip()

                    #Check for missing data
                    if not question_text or any(pd.isna(choice) for choice in choices.values()) or pd.isna(correct_answer) or pd.isna(subject_category): 
                        raise ValueError(f"Missing data in row{index}:Question or choices or correct answer of subject_category are incomplete")

                    subject_category,created= SubjectCategory.objects.get_or_create(
                        name=subject_category,
                        questions_file=self
                    )
                    question,created= Question.objects.get_or_create(
                        questions_file=self,
                        text=question_text,
                        subject_category=subject_category
                    )
                    #Handle question images
                    if 'QuestionImages' in row and pd.notna(row['QuestionImages']):
                        print("✅ 'QuestionImages' column found and not empty")

                        image_paths = str(row['QuestionImages']).split(',')
                        print(f"Image Paths for Question '{question_text}': {image_paths}")


                        for img_path in image_paths:
                            img_path = img_path.strip()
                            print(f"🔍 Processing image path: '{img_path}'")
                            if not img_path:
                                print(f"Empty image path found for question '{question_text}'")
                                continue

                            # Resolve the full path relative to the Excel file's directory
                            # full_img_path = os.path.normpath(os.path.join(excel_dir, img_path))
                            local_path=r"G:\PYQ-ExcelAndMedias\ExcelConvertable\images"
                            full_img_path = os.path.normpath(os.path.join(local_path, img_path))
                            print(f"Checking Image Path: {full_img_path}")

                            #Check if the image file exists
                            if os.path.exists(full_img_path):
                                print("✅ Image file exists")
                                try:
                                    with open(full_img_path, 'rb') as f:
                                        image_file = File(f, name=os.path.basename(full_img_path))

                                        print(f"📦 Image file loaded: {image_file.name}")


                                         # Optional: print image size to confirm it's not empty
                                        f.seek(0, os.SEEK_END)
                                        file_size = f.tell()
                                        print(f"📏 File size: {file_size} bytes")

                                        # Go back to start
                                        f.seek(0)

                                        image_obj, created = Image.objects.get_or_create(
                                            question=question,
                                            image=image_file
                                        )
                                        print(f"Image Saved: {image_obj.image.url} (Created: {created})")
                                except Exception as e:
                                    print(f"Error opening image file '{full_img_path}': {e}")
                            else:
                                print(f"Image file not found: {full_img_path}")
                    else:
                        print(f"❌ 'QuestionImages' column missing or empty for question: {question_text}")



                    
                    for choice_key , choice_text in choices.items():
                        is_correct=(choice_key==correct_answer)
                        Choice.objects.get_or_create(question=question, text=choice_text,is_correct=is_correct)


                except Exception as e:
                    print (f"Error processing row {index}: {e}, Row data : {row}")
        except Exception as e:
            print(f"Error importing quiz:{e}")

class SubjectCategory(models.Model):
    name=models.CharField(max_length=100)
    questions_file=models.ForeignKey(Questions_file,on_delete=models.CASCADE,related_name='subject_category')

    class Meta:
        verbose_name_plural='SubjectCategories'

    def __str__(self):
        return f"{self.questions_file.title}, {self.name}"


class Question(models.Model):
    questions_file=models.ForeignKey(Questions_file,on_delete=models.CASCADE)
    text=models.TextField()
    subject_category=models.ForeignKey(SubjectCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:50]
    

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    text=models.TextField(max_length=255)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"    
    

User=get_user_model()    
class UserResponse(models.Model):   ##for particular question
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='response')  
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    selected_choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    is_correct=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    is_submitted=models.BooleanField(default=False)

    class Meta:
        unique_together=('user','question')

    def save(self,*args,**kwargs):
        self.is_correct=self.selected_choice.is_correct
        super().save(*args,**kwargs)
        if self.is_submitted:
            self.update_quiz_result()


    def update_quiz_result(self):
        result,_=UserQuizResult.objects.get_or_create(
            user=self.user,
            questions_file=self.question.questions_file
        )
        result.update_points()


class UserQuizResult(models.Model):  ##for particular question file
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz_results')
    questions_file=models.ForeignKey(Questions_file, on_delete=models.CASCADE, related_name='results')
    points=models.IntegerField(default=0)
    completed_at=models.DateTimeField(null=True,blank=True)


    class Meta:
        unique_together=('user','questions_file')


    def update_points(self):
        correct_count=UserResponse.objects.filter(
            user=self.user,
            question__questions_file=self.questions_file,
            is_correct=True,
            is_submitted=True

            ).count()

        self.points=correct_count*1
        self.save()
        self.update_leaderboard()

    def update_leaderboard(self):
        leaderboard, _ =Leaderboard.objects.get_or_create(user=self.user)
        leaderboard.update_total()


class Leaderboard(models.Model): ##as you know its leaderboard
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='leaderboard_entries')
    total_points=models.IntegerField(default=0)
    last_updated=models.DateTimeField(auto_now=True)

    def update_total(self):
        self.total_points=UserQuizResult.objects.filter(user=self.user).aggregate(
            total=models.Sum('points')
        )['total'] or 0
        self.save()








