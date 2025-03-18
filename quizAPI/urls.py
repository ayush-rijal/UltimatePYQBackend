from django.urls import path
from .views import AllQuestionAPIView, AQuestionAPIView,AllChoiceOfAQuestionAPIView,AllCategory0APIView,AllCategory1APIView,AllQuestions_fileAPIView

urlpatterns = [
    path('category0/', AllCategory0APIView.as_view()),  ##gives all the categories like Medical,Engineering,Loksewa present in the database under domain/quizapi/category0

    path('<str:category0>/', AllCategory1APIView.as_view()),  ##gives all the categories like IOM , CEE , IOE present in the database under domain/quizapi/Medical

    path('<str:category0>/<str:category1>/', AllQuestions_fileAPIView.as_view()), ###gives all the questions file present in the database for the specific category like IOM2019 , IOM 2018 , IOE2017 under domain/quizapi/Medical/IOM

    path('<str:category0>/<str:category1>/<str:questions_file>/',AllQuestionAPIView.as_view()),   ##gives every question present in the database with pagination under domain/quizapi/Medical/IOM/IOM2019

    path('<str:category0>/<str:category1>/<str:questions_file>/<int:pk>/', AQuestionAPIView.as_view()), ##gives the specific question with its ID under domain/quizapi/Medical/IOM/IOM2019/1


    path('<str:category0>/<str:category1>/<str:questions_file>/<int:pk>/choices/',AllChoiceOfAQuestionAPIView.as_view()), ##gives all the choices for the specific question under domain/quizapi/category0/IOM/IOM2019/1/choices
    
]
