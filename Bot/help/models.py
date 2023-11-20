from django.db import models
from django.http import QueryDict, HttpResponse, HttpRequest
from enum import Enum
from django.shortcuts import render
from authentication.models import *
from django.utils.safestring import mark_safe
from Bot.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, BASE_DIR
import bots

class QuestionType(Enum):
    MATH_STRING = 1
    NEWS = 2
    MATH_WORD_PROBLEM = 3
    GRAMMAR_CHECK = 4
    SUMMARIZER = 5
    GRAPHS = 6

QUESTION_OPTIONS = [ 
        (QuestionType.MATH_STRING.value, "Math Expression or Conversion"),
        (QuestionType.NEWS.value, "Current Events"),
        (QuestionType.MATH_WORD_PROBLEM.value, "Math Word Problem"),
        (QuestionType.GRAMMAR_CHECK.value, "Grammar Check"),
        (QuestionType.SUMMARIZER.value, "Summarize Text"),
        (QuestionType.GRAPHS.value, "Graph Images"),
]

def resolve_question_request(request: HttpRequest, request_data: QueryDict) -> HttpResponse:
        # maybe change to some other check from the request data
    question_type = request_data.get("questionType")
    if question_type == "None":
        response = HttpResponse()
        return response
    question_type = int(question_type)
    match question_type:
        case QuestionType.MATH_STRING.value | QuestionType.MATH_WORD_PROBLEM.value | QuestionType.GRAMMAR_CHECK.value | QuestionType.SUMMARIZER.value:
            return TextQuestionTextAnswer.ask(request, request_data)
        case QuestionType.GRAPHS.value:
            return EquationQuestionImageAnswer.ask(request, request_data)

    response = HttpResponse()
    return response

class TextQuestionTextAnswer(models.Model):
    question_type = models.IntegerField(choices=QUESTION_OPTIONS)
    question = models.CharField(max_length=2048)
    answer = models.CharField(max_length=2048)
    date_asked = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="text_question_test_answers")

    class Meta:
        ordering = ['-date_asked']

    def ask(request: HttpRequest, request_data: QueryDict) -> HttpResponse:
        question = None
        answer = None
        question_type = int(request_data.get("questionType"))
        question, answer = TextQuestionTextAnswer.generate_answer_question(request_data)
        if question == '' or answer is None:
            safe_html = mark_safe('''<h4 class="text-center">Your answer will appear here</h4>''')
            response = HttpResponse(safe_html)
            return response

        asked_question = TextQuestionTextAnswer(
            question_type = question_type,
            question=question,
            answer=answer,
            student=request.user.student)
        asked_question.save()
        context = {
            "question": question,
            "answer": answer,
            "date_asked": asked_question.date_asked
        }
        return render(request, 'answer_text.html', context=context)

    def generate_answer_question(request_data: QueryDict) -> tuple[str, str]:
        question_type = int(request_data.get("questionType"))
        match question_type:
            case QuestionType.MATH_STRING.value:
                question = request_data.get("expression")
                stored_response = TextQuestionTextAnswer.objects.filter(
                    question_type = question_type,
                    question=question,
                ).first()
                if stored_response: return question, stored_response.answer
                answer = bots.getMathStringAnswer(question, 5)
                answer = answer.result
            case QuestionType.MATH_WORD_PROBLEM.value:
                question = request_data.get("problem")
                stored_response = TextQuestionTextAnswer.objects.filter(
                    question_type = question_type,
                    question=question,
                ).first()
                if stored_response: return question, stored_response.answer
                answer = bots.answer_word_problem(question)
            case QuestionType.GRAMMAR_CHECK.value:
                question = request_data.get("text")
                answer = bots.correct_grammar(stored_response)
            case QuestionType.SUMMARIZER.value:
                question = request_data.get("text")
                answer = bots.summarizer(question)[0]['summary_text']
        return question, answer

class EquationQuestionImageAnswer(models.Model):
    is_plot = models.BooleanField()
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    date_asked = models.DateTimeField(auto_now_add=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="equation_question_image_answers")

    def get_path(question: str):
        return str( BASE_DIR / "static" / (question + ".png"))
    
    def rel_path(self):
        return "/" + self.question + ".png"

    def ask(request: HttpRequest, request_data: QueryDict) -> HttpResponse:
        a = request_data.get("a")
        b = request_data.get("b")
        c = request_data.get("c")
        d = request_data.get("d")
        e = request_data.get("e")
        is_plot = request_data.get("isPlot") != None
        question: str = "_".join([a,b,c,d,e])

        existing_graph = EquationQuestionImageAnswer.objects.filter(
            question=question,
            is_plot=is_plot
        ).first()
        if not existing_graph:
            x_min = request_data.get("x_min")
            x_max = request_data.get("x_max")
            x_range = range(int(x_min), int(x_max))
            equation = bots.equationMakerABCDE(int(a), int(b), int(c), int(d), int(e))
            bots.plotter(equation, x_range, EquationQuestionImageAnswer.get_path(question))
        answer = EquationQuestionImageAnswer.get_path(question)
        new_graph = EquationQuestionImageAnswer(
            question=question,
            is_plot=is_plot,
            answer=answer,
            student=request.user.student
        )
        new_graph.save()

        context = {
            "question": question,
            "answer": new_graph.rel_path(),
            "date_asked": new_graph.date_asked
        }

        return render(request, 'answer_image.html', context=context)



