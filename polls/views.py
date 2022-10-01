# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #return last 5 questions
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the back button <------------------------------------
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # That code loads the template called polls/index.html and passes it a context.
    # The context is a dictionary mapping template variable names to Python objects.

    # The render() function takes the request object as its first argument,
    # a template name as its second argument and a dictionary as its optional third argument.
    # It returns an HttpResponse object of the given template rendered with the given context.
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

    return HttpResponse(template.render(context, request))


############# My own method to reduce typing redundant code: ################################
def ret_render(request, question_id, view):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, f'polls/{view}.html', {'question': question})


def detail(request, question_id):
    # The view raises the Http404 exception
    # if a question with the requested ID doesn’t exist.
    # try:
    #    question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #    raise Http404("Question does not exist."
    # return HttpResponse("You're looking at question %s" % question_id
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})
    return ret_render(request, question_id, 'detail')


def results(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})
    return ret_render(request, question_id, 'results')
'''
