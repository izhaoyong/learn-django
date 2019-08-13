from django.urls import path

from . import views


urlpatterns = [
	# ex: /polls/
	path('', views.index, name='index'),
	path('template/', views.template, name='template'),
	path('render/', views.render_template, name='render_template'),

	# ex: /polls/5/，这里的int:不是必需的，可以省略
	path('<int:question_id>', views.detail, name='detail'),

	# ex: /polls/5/results/
	path('<int:question_id>/results', views.results, name='results'),

	# ex: /polls/5/vote
	path('<int:question_id>/vote', views.vote, name='vote'),

	# ex: /polls/query?name=123&key=sss&name=345
	path('query', views.query, name='query'),

	# ex: /polls/body
	path('body/', views.body, name='body'),
]
