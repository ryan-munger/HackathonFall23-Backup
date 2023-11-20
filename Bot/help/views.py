from enum import Enum
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required
from .models import *


@login_required
def question_history(request: HttpRequest) -> HttpResponse:
    context = {
        "student": request.user.student
    }
    return render(request, 'history.html', context=context)

@login_required
def ask_question(request: HttpRequest) -> HttpResponse:
    context = {
        "questionOptions": QUESTION_OPTIONS
    }
    return render(request, 'question.html', context=context)

def get_question_area(request: HttpRequest) -> HttpResponse:
    data = QueryDict(request.body)
    question_type = data.get("questionType")
    if question_type == "None":
        response = HttpResponse()
        response['HX-Trigger'] = 'noop'
        return response
    question_type = int(question_type)
    context = {"question_type": question_type}
    match question_type:
        case QuestionType.MATH_STRING.value:
            return render(request, "math_expression.html", context=context)
        case QuestionType.MATH_WORD_PROBLEM.value:
            return render(request, "math_word_problem.html", context=context)
        case QuestionType.GRAMMAR_CHECK.value:
            return render(request, "grammar_check.html", context=context)
        case QuestionType.SUMMARIZER.value:
            return render(request, "summarize.html", context=context)
        case QuestionType.GRAPHS.value:
            return render(request, "graphs.html", context=context)

    safe_html = mark_safe('''<h4 class="text-center">Your question box will appear here</h4>''')
    response = HttpResponse(safe_html)
    return response


def answer_question(request: HttpRequest) -> HttpResponse:
    data = QueryDict(request.body)
    return resolve_question_request(request, data)
