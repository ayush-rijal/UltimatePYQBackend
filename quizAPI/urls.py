from django.urls import path,re_path
from .views import AllQuestionAPIView, AQuestionAPIView,AllChoiceOfAQuestionAPIView,AllCategoriesAPIView,AllQuestions_fileAPIView
from .views import QuizResultAPIView,GlobalLeaderboardAPIView,SubmitQuizAPIView
# from .views import SubmitAnswerAPIView
from .views import CategoryChildrenAPIView,AllQuestions_fileAPIView

urlpatterns = [

    re_path(r'^leaderboard/$', GlobalLeaderboardAPIView.as_view(), name='global-leaderboard'),

    
    re_path(r'^(?P<category_path>[\w/]+)/files/$', AllQuestions_fileAPIView.as_view(), name='questionsfile-list'),

    ##Root categories only
    path('categories/', AllCategoriesAPIView.as_view(), name='category-list'),

    ##Children of a category
    re_path(r'^(?P<category_path>[\w/]+)/$', CategoryChildrenAPIView.as_view(), name='category-children'), #(?P<category_path>[\w/]+) → Captures letters, numbers, underscores, or /

    ##quiz files for a category
    re_path(r'^(?P<category_path>[\w/]+)/files/$', AllQuestions_fileAPIView.as_view(), name='questionsfile-list'), ##[\w-] includes letters, numbers, underscores, and -, but not spaces.

    #questions in a quiz file
    re_path(r'^(?P<category_path>[\w/]+)/(?P<questions_file>[^/]+)/$', AllQuestionAPIView.as_view(), name='question-list'),  ##[^/]+ means "match any character except /", which includes spaces, letters, numbers, etc

    #single question in a quiz file
    re_path(r'^(?P<category_path>[\w/]+)/(?P<questions_file>[^/]+)/question/(?P<pk>\d+)/$', AQuestionAPIView.as_view(), name='question-detail'),

    #choices for a question
    re_path(r'^(?P<category_path>[\w/]+)/(?P<questions_file>[^/]+)/question/(?P<pk>\d+)/choices/$', AllChoiceOfAQuestionAPIView.as_view(), name='choice-list'),

   #submit quiz
    re_path(r'^(?P<category_path>[\w/]+)/(?P<questions_file>[^/]+)/submit/$', SubmitQuizAPIView.as_view(), name='submit-quiz'),

    #quiz result
    re_path(r'^(?P<category_path>[\w/]+)/(?P<questions_file>[^/]+)/result/$', QuizResultAPIView.as_view(), name='quiz-result'),

    # Global leaderboard
    re_path(r'^leaderboard/$', GlobalLeaderboardAPIView.as_view(), name='global-leaderboard'),
]




