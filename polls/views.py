from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Question 
from django.views import generic

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:2]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)
def detail(request, question_id):
	question  = get_object_or_404(Question,pk=question_id)
	context = {'question' : question}
	return render(request,'polls/detail.html',context)
	

def results(request, question_id):
	question = get_object_or_404(Question,pk = question_id)
	return render(request,"polls/results.html",{'question':question})


def vote(request, question_id):
	question = get_object_or_404(Question,pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except(KeyError,Choice.DoesNotExist):
		return render(request,"polls/details.html",{
			"question" : question,
			"Error_message":"You Didnt select a choice."
			})
	selected_choice.vote+=1
	selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))