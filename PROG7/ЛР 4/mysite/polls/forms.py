from django import forms


class QuestionCreateForm(forms.Form):
    """
    Форма для создания нового опроса.

    - question_text: заголовок вопроса
    - choices_text: варианты ответов, по одному на строку
    """

    question_text = forms.CharField(
        label="Вопрос",
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Введите текст вопроса"}),
    )
    choices_text = forms.CharField(
        label="Варианты ответа",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Каждый вариант ответа на отдельной строке",
                "rows": 5,
            }
        ),
    )


