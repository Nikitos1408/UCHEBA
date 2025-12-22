import random
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View, generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User

from .forms import NewUserForm

from .models import Choice, Question
from .forms import QuestionForm


SLOGANS = [
    "Polls or Trolls: Without your choice, beware the gremlins' voice!",
    "Polls or Spooks: Don't let phantoms choose your folks!",
    "Polls or Ghouls: Vote or let the underworld fool!",
    "Polls or Wraiths: Make a choice or invite spectral straits!",
    "Polls or Shadows: Without your say, darkness grows!",
    "Polls or Beasts: Choose wisely, or unleash monstrous feasts!",
    "Polls or Nightmares: Cast your vote, or fall into horror's lairs!",
    "Polls or Ghosts: Decide or invite the haunted costs!",
    "Polls or Fiends: Without your voice, chaos reigns!",
    "Polls or Vampires: Your choice could calm the nocturnal pyres!",
    "Polls or Goblins: Without a vote, mischief unfolds in!",
    "Polls or Crows: Cast your choice or let dark omens rise!",
    "Polls or Skeletons: A vote unsaid releases bone-ridden threats!",
    "Polls or Serpents: Fail to choose, and risk subterranean events!",
    "Polls or Abyss: A silent electorate summons the darkness!"
]


class PollsBaseView(View):
    slogans = SLOGANS

    def get_slogan(self):
        return random.choice(self.slogans)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slogan'] = self.get_slogan()
        return context


class IndexView(PollsBaseView, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(PollsBaseView, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(PollsBaseView, generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class StatisticsView(View):
    def get(self, request, *args, **kwargs):
        context = {'message': 'Привет, это GET-запрос!'}
        return render(request, 'polls/statistics.html', context)

    def post(self, request, *args, **kwargs):
        context = {'message': 'Привет, это POST-запрос!'}
        return render(request, 'polls/statistics.html', context)


class VoteView(PollsBaseView, View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(
                request,
                "polls/detail.html",
                {
                    "slogan": self.get_slogan(),
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class UserIsStaffMixin(UserPassesTestMixin):
    login_url = "polls:login"
    redirect_field_name = "next"
    raise_exception = False

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        # next_url = self.request.path
        # return redirect(self.login_url, f"{self.redirect_field_name}={next_url}")
        return redirect_to_login(self.request.get_full_path(), self.login_url, self.redirect_field_name)
        # return redirect('{}?{}={}'.format(reverse(self.login_url), self.redirect_field_name, next_url))


class PollNewView(PollsBaseView, UserIsStaffMixin, LoginRequiredMixin, View):
    
    def get(self, request):
        form = QuestionForm()
        return render(
            request,
            'polls/poll_new_edit.html',
            {
                'form': form,
                "slogan": self.get_slogan(),
            }
        )

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.save()
            return redirect('polls:detail', pk=poll.pk)
        return render(
            request,
            'polls/poll_new_edit.html',
            {
                'form': form,
                "slogan": self.get_slogan(),
            }
        )

class PollEditView(PollsBaseView, UserIsStaffMixin, LoginRequiredMixin, View):
    
    def get(self, request, pk):
        poll = get_object_or_404(Question, pk=pk)
        form = QuestionForm(instance=poll)
        return render(
            request, 'polls/poll_new_edit.html', {
                "slogan": self.get_slogan(),
                'form': form
            }
        )

    def post(self, request, pk):
        poll = get_object_or_404(Question, pk=pk)
        form = QuestionForm(request.POST, instance=poll)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.pub_date = timezone.now()
            poll.save()
            return redirect('polls:detail', pk=poll.pk)
        return render(
            request, 'polls/poll_new_edit.html', {
                "slogan": self.get_slogan(),
                'form': form
            }
        )


class LoginView(PollsBaseView, View):
    logger = logging.getLogger(__name__)
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request=request, template_name="polls/login.html", context={"login_form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                next_url = self.request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('polls:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        
        slogan = self.get_slogan()
        # logger.warning(f"Slogan {slogan}.")
        return render(
            request=request,
            template_name="polls/login.html",
            context={
                "slogan": slogan,
                "login_form": form
            }
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("polls:index")


class AccountRegisterView(View):
    form_class = NewUserForm
    template_name = "polls/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request=request, template_name=self.template_name, context={"register_form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(request)
            messages.success(request, f"Registration successful. Please go to your '{user.email}' e-mail inbox messages to activate the account.")
            return redirect("polls:index")

        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name=self.template_name, context={"register_form": form})


class AccountActivationView(View):
    def get(self, request, uidb64, token):
        # messages.error(request, f"uidb64 = {uidb64}, token = {token}")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            # messages.error(request, f"uid = {uid}")
            user = User.objects.get(pk=uid)
            # messages.error(request, f"user = {user}")
        except:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'polls/account_activation_success.html')
        else:
            return render(request, 'polls/account_activation_failure.html')


# =================================================================================

from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import parsers, status
from datetime import datetime, timedelta
from django.utils import timezone
from .serializers import QuestionSerializer
from .models import Question

class QuestionView(APIView):
    parser_classes = (parsers.JSONParser,)
    
    def post(self, request, format=None):
        # Получение данных из тела POST-запроса
        request_data = request.data
        
        date_range_provided = ('publication-dates' in request_data) \
            and ('from' in request_data['publication-dates'] and 'to' in request_data['publication-dates'])
        
        date_range = None
        if date_range_provided:
            publication_dates = request_data['publication-dates']
            date_from = datetime.strptime(publication_dates['from'], '%Y-%m-%d')
            date_from = date_from.replace(hour=0, minute=0, second=0)
            date_to = datetime.strptime(publication_dates['to'], '%Y-%m-%d')
            date_to = date_to.replace(hour=23, minute=59, second=59)
            date_range = [date_from, date_to]
        else:
            date_now = timezone.now()
            date_from = (date_now - timedelta(days=60)).replace(hour=0, minute=0, second=0)
            date_to = date_now.replace(hour=23, minute=59, second=59)
            date_range = [date_from, date_to]
        
        tz = timezone.get_current_timezone()
        
        # Запрос в базу данных по интервалу дат публикации
        questions = Question.objects.filter(pub_date__range=date_range)
        
        print(f"Questions: {questions}")

        # Сериализация данных и создание нового вопроса
        question_serializer = QuestionSerializer(questions, many=True)
        # question_serializer.is_valid()
        # question_serializer.save()
        # print(f"Serializer errors: {question_serializer.errors}")
        # if question_serializer.is_valid():
        #     question_serializer.save()
        #     print("SAVED")
        # else:

        print(f"Serialized: {question_serializer.data}")
            
        response_data = {
            'publication-dates': {
                'from': date_range[0],
                'to': date_range[1]
            },
            'questions': question_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

        # return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =================================================================================


from django.utils import timezone
from django.http import JsonResponse
from django.contrib import admin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question, Choice

import matplotlib.pyplot as plt
import io
import csv
from django.db.models import Sum


class QuestionStatsAPIView(APIView):
    """
    Микросервис статистики по одному голосованию.
    Возвращает количество голосов и процент для каждого варианта ответа,
    а также SVG-гистограмму распределения голосов.
    """

    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response("Question does not exist", status=status.HTTP_404_NOT_FOUND)

        choices = question.choice_set.all()
        total_votes = sum(choice.votes for choice in choices)

        stats = {
            'question_id': question.pk,
            'question': question.question_text,
            'total_votes': total_votes,
            'choices': []
        }

        for choice in choices:
            choice_percentage = (choice.votes / total_votes) * 100 if total_votes != 0 else 0
            stats['choices'].append({
                'choice_id': choice.pk,
                'choice_text': choice.choice_text,
                'votes': choice.votes,
                'percentage': round(choice_percentage, 2),
            })

        if choices:
            most_popular_choice = max(choices, key=lambda choice: choice.votes)
            least_popular_choice = min(choices, key=lambda choice: choice.votes)

            stats['most_popular_choice'] = most_popular_choice.choice_text
            stats['least_popular_choice'] = least_popular_choice.choice_text
        else:
            stats['most_popular_choice'] = None
            stats['least_popular_choice'] = None

        # Построение гистограммы распределения голосов
        fig, ax = plt.subplots()
        plt.style.use('ggplot')
        ax.bar([choice.choice_text for choice in choices], [choice.votes for choice in choices])
        plt.xticks(rotation=20)
        plt.xlabel('Choices')
        plt.ylabel('Votes')
        plt.title('Votes Distribution')
        plt.subplots_adjust(bottom=0.2)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='svg')
        plt.close(fig)
        buffer.seek(0)

        stats['histogram_svg'] = buffer.getvalue().decode()

        return Response(stats)


class PollsStatisticsAPIView(APIView):
    """
    Микросервис агрегированной статистики по всем голосованиям.

    Поддерживаемые query-параметры:
    - date_from, date_to: фильтрация по дате публикации (формат YYYY-MM-DD)
    - order_by: способ сортировки:
        * date  — по дате публикации (по убыванию)
        * votes — по общему количеству голосов (по убыванию)
        * popularity — то же, что и votes (синоним)
    """

    def get_queryset(self, request):
        qs = Question.objects.all()

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        if date_from:
            qs = qs.filter(pub_date__date__gte=date_from)
        if date_to:
            qs = qs.filter(pub_date__date__lte=date_to)

        order_by = request.query_params.get('order_by')
        if order_by in ('votes', 'popularity'):
            qs = qs.annotate(total_votes=Sum('choice__votes')).order_by('-total_votes', '-pub_date')
        elif order_by == 'date':
            qs = qs.order_by('-pub_date')

        return qs

    def get(self, request):
        questions = self.get_queryset(request)

        total_polls = questions.count()
        total_votes_all = 0
        questions_stats = []

        for question in questions:
            choices = question.choice_set.all()
            total_votes = sum(choice.votes for choice in choices)
            total_votes_all += total_votes

            q_stats = {
                'question_id': question.pk,
                'question_text': question.question_text,
                'pub_date': question.pub_date,
                'total_votes': total_votes,
                'choices': [],
            }

            for choice in choices:
                percentage = (choice.votes / total_votes) * 100 if total_votes != 0 else 0
                q_stats['choices'].append({
                    'choice_id': choice.pk,
                    'choice_text': choice.choice_text,
                    'votes': choice.votes,
                    'percentage': round(percentage, 2),
                })

            questions_stats.append(q_stats)

        response_data = {
            'total_polls': total_polls,
            'total_votes': total_votes_all,
            'questions': questions_stats,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PollsExportAPIView(APIView):
    """
    Микросервис экспорта данных о голосованиях.

    Поддерживаемые query-параметры:
    - format: json (по умолчанию) или csv
    - те же, что и у PollsStatisticsAPIView: date_from, date_to, order_by.
    """

    def get_queryset(self, request):
        # Используем тот же фильтр, что и в PollsStatisticsAPIView
        return PollsStatisticsAPIView().get_queryset(request)

    def get(self, request):
        export_format = request.query_params.get('format', 'json').lower()
        questions = self.get_queryset(request)

        # Собираем те же данные, что и в агрегированной статистике
        questions_stats = []
        for question in questions:
            choices = question.choice_set.all()
            total_votes = sum(choice.votes for choice in choices)
            q_stats = {
                'question_id': question.pk,
                'question_text': question.question_text,
                'pub_date': question.pub_date,
                'total_votes': total_votes,
                'choices': [],
            }
            for choice in choices:
                percentage = (choice.votes / total_votes) * 100 if total_votes != 0 else 0
                q_stats['choices'].append({
                    'choice_id': choice.pk,
                    'choice_text': choice.choice_text,
                    'votes': choice.votes,
                    'percentage': round(percentage, 2),
                })
            questions_stats.append(q_stats)

        if export_format == 'csv':
            # Экспорт в CSV: каждая строка — один вариант ответа
            from django.http import HttpResponse

            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="polls_export.csv"'

            writer = csv.writer(response)
            writer.writerow([
                'question_id',
                'question_text',
                'pub_date',
                'choice_id',
                'choice_text',
                'votes',
                'percentage',
            ])

            for q in questions_stats:
                for choice in q['choices']:
                    writer.writerow([
                        q['question_id'],
                        q['question_text'],
                        q['pub_date'],
                        choice['choice_id'],
                        choice['choice_text'],
                        choice['votes'],
                        choice['percentage'],
                    ])

            return response

        # По умолчанию — JSON-экспорт
        return Response({'questions': questions_stats}, status=status.HTTP_200_OK)


# =================================================================================








# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("polls:index")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="polls/login.html", context={"login_form": form})


# def logout_request(request):
# 	logout(request)
# 	messages.info(request, "You have successfully logged out.") 
# 	return redirect("polls:index")

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

