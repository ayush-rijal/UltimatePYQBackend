

# Create your tests here.
from quizAPI.models import UserQuizResult, Questions_file, Category
from django.contrib.auth.models import User
from django.utils import timezone
user = User.objects.get(username='tai')
category = Category.objects.create(name='TestCategory')
questions_file = Questions_file.objects.create(title='TestQuiz', category=category)
UserQuizResult.objects.create(
    user=user,
    questions_file=questions_file,
    points=10,
    completed_at=timezone.now()
)