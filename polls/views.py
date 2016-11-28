from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Question
from .models import Choice


def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    ctx = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', ctx)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    ctx = {'question':question}
    return render(request, 'polls/detail.html', ctx)


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)

    try :
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        ctx = {'question':p, 'error_message':"You didn't select choice"}
        return render(request, 'polls/detail.html', ctx)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    ctx = {'question':question}
    return render(request, 'polls/results.html', ctx)