from django.urls import include, path, re_path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
    path("new/", views.PollNewView.as_view(), name="poll_new"),
    # ex: /polls/5/edit/
    path('<int:pk>/edit/', views.PollEditView.as_view(), name='poll_edit'),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.AccountRegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>", views.AccountActivationView.as_view(), name="activate"),
    
    path("statistics", views.StatisticsView.as_view(), name="statistics"),
    path("statistics-question-list", views.QuestionView.as_view(), name="statistics-question-list"),
    path('statistics/question-stats/<int:pk>/', views.QuestionStatsAPIView.as_view(), name='statistics-question-stats'),

    # DRF микросервисы для статистики и экспорта данных по голосованиям
    path('api/statistics/', views.PollsStatisticsAPIView.as_view(), name='api-statistics'),
    path('api/export/', views.PollsExportAPIView.as_view(), name='api-export'),
]
