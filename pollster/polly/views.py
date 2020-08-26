from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Question, Choice


def index(request):
    questions = Question.objects.order_by('-pub_date')[:5]
    context = {'questions': questions}
    return render(request, 'polly/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polly/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polly/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polly/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polly:results', args=(question.id,)))


def resultsdata(request, obj):
    vote_data = []
    question = Question.objects.get(pk=obj)
    votes = question.choice_set.all()

    for i in votes:
        vote_data.append({i.choice_text: i.votes})

    print(vote_data)
    return JsonResponse(vote_data, safe=False)
