from django.db import models
import pandas as pd
from django.contrib.auth import get_user_model

class Category0(models.Model):
    name=models.CharField(max_length=15)

    class Meta:
        verbose_name_plural='Categories0'
    def __str__(self):
        return self.name    


class Category1(models.Model):
    name=models.CharField(max_length=15)
    category0=models.ForeignKey(Category0,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural= 'Categories1'
    def __str__(self):
        return self.name
    
class Questions_file(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    category0=models.ForeignKey(Category0,on_delete=models.CASCADE)
    category1=models.ForeignKey(Category1,on_delete=models.CASCADE)
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
            for index, row in df.iterrows():
                try:
                    question_text=str(row['Question']).strip()
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








