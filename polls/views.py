from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import User

# Create your views here.


def index(request):
	print(User.objects.using('soda').all())

	template = loader.get_template('polls/index.html')
	context = {}
	return HttpResponse(template.render(context, request))


def template(request):
	template = loader.get_template('polls/template.html')
	context = {}
	return HttpResponse(template.render(context, request))


def render_template(request):

	return render(request, 'polls/render.html', {})




def detail(request, question_id):
	print(question_id)
	return HttpResponse(question_id)


def results(request, question_id):
	return HttpResponse(question_id)

def vote(request, question_id):
	return HttpResponse(question_id)

def query(request):
	nameDict = request.GET
	# print(request.path)
	# print(request.path_info)
	# print(request.method)
	print(request.GET)
	# print(request.META)
	print(nameDict.getlist('name'))

	return HttpResponse(request.GET)


@csrf_exempt
def body(request):
	nameDict = request.POST
	print(request.body.decode())

	return HttpResponse('23')
