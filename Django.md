# Django学习笔记



### 安装

Django是一个pip的库，可以通过pip进行安装：

```
pip install django
```



### 新建project

1. django-admin startproject project-name(工程名不能有中横线)
2. python -m django startproject project-name



### 启动服务

首先进入到上一步建立的project-name中，里面有一个__manage.py__文件

```
python manage.py runserver
```

完整版命令：

```
python manage.py runserver HOST(0.0.0.0):PORT(8000)
python manage.py runserver PORT(8000)
```

其中HOST是ip地址，默认是本地可访问，如果想所有机器可访问可以写成__0.0.0.0__

PORT是服务监听的端口。

比如：

- 启动8088端口的服务

```
python manage.py runserver 8088
```

- 任意地址都可以访问的

```
python manage.py runserver 0.0.0.0:8900
```



### 创建应用

当我们要提供服务时，具体的是对应到某个应用下的服务。所以我们需要先创建应用

```
			python -m django startapp app-name
或者	 python manage.py startapp app-name
```

例子：python -m django startapp polls，就是创建了一个polls的应用。提供具体的服务我们就在这些__应用__中写逻辑。



### 设置路由

无论我们是想访问页面还是发送HTTP请求，都需要知道具体的路径，就是域名后面的？之前的路径，在Django里被称为__路由__。

路由可以简单分为project路由以及app路由（这个不是官方下的定义，是我自己为了好记这样划分的）。

project路由可以算是全局路由，在startproject创建的目录下，文件名为urls.py。app路由在startapp目录下的urls.py中。

如果按返回的页面还是接口数据来划分可以设置视图路由和接口路由。

#### 视图路由

是访问某个具体页面的路径。比如说要访问__home__页面。就需要配置home的视图路由了。

比如说我们在polls应用的设置home路由。首先我们修改polls/views.py的文件。添加某个函数并且返回HttpResponse请求；

#### 接口路由

原理同上。

>  基本语法:path(route, view, kwargs(optional), name(optional))

- route：可以简单的理解为url中的路径

- view：视图函数来处理匹配成功的路由

- kwargs：传入的参数

- name：路由指定一个名字

  

### 获取请求参数

配置好相应的路由，以及处理函数后，我们还需要获取到一些参数，才能处理更多的情况。

- 路由中的参数

  一般写到path的route参数中，然后在处理函数中指明相应的处理函数。

  > __polls/urls.py__文件

  ```
  from django.urls import path
  
  from . import views
  
  urlpatterns = [
      # ex: /polls/
      path('', views.index, name='index'),
      # ex: /polls/5/
      path('<int:question_id>/', views.detail, name='detail'),
      # ex: /polls/5/results/
      path('<int:question_id>/results/', views.results, name='results'),
      # ex: /polls/5/vote/
      path('<int:question_id>/vote/', views.vote, name='vote'),
  ]
  ```

  > __polls/views.py__文件

  ```
  def detail(request, question_id):
      return HttpResponse("You're looking at question %s." % question_id)
  
  def results(request, question_id):
      response = "You're looking at the results of question %s."
      return HttpResponse(response % question_id)
  
  def vote(request, question_id):
      return HttpResponse("You're voting on question %s." % question_id)
  ```

  从上面两个文件可以看出来，在路径上设置的参数，需要在处理函数中制定参数







- 获取GET请求参数
- 获取POST请求参数