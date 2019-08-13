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

  从上面两个文件可以看出来，在路径上设置的参数，需要在处理函数中指定同名的参数。
  
  比如：detail的路由规则和处理函数
  
  > polls/urls.py
  
  ```
  path('<int:question_id>/', views.detail, name='detail')
  ```
  
  >polls/views.py
  
  ```
  def detail(request, question_id):
  		return HttpResponse(question_id)
  ```
  
  这里question_id在这两个函数中必须一样，才不会有错。但是前面的__类型说明不是必需的__。

- 获取GET请求参数

  通过使用request.GET方法获取相应的参数

  > polls/urls.py文件

  ```
  # ex: /polls/query?name=123&key=sss&name=345
  	path('query', views.query, name='query'), 注意这里不能在前面添加 "/"，
  ```

  > polls/views.py

  ```
  def query(request):
  	name = request.GET['name']
  	print(name)
  	return HttpResponse(request.GET['key'])
  ```

  这里request.GET返回的是QueryDict类型的数据类型。每个key对应的value是一个列表，但是如果直接获取数据时返回的是列表最后一个值。

  比如query：__name=123&key=ad132123&name=35__，对应的QueryDict是__<QueryDict: {'name': ['123', '35'], 'key': ['ad132123']}>__，当我们获取数据时：request.GET['name']返回的是35，就是列表最后一个值。如果想获取123和35需要用到__request.GET.getlist(key)__。

- 获取POST请求参数

  通过使用request.POST方法获取相应的参数，情况类似request.GET，返回的也是QueryDict数据类型。但是如果数据类型是application/json（heander中的Content-Type的值是application/json）时，request.POST是获取不到的。如果想获取具体的值需要通过request.body。将request.body转化为json字符串就可以获得具体的值了。

  > 发送POST请求时会遇到csrf的问题，需要在post函数添加csrf_exempt的修饰函数。将csrf过滤掉。

  > polls/views.py

  ```
  from django.views.decorators.csrf import csrf_exempt
  
  @csrf_exempt
  def body(request):
  	nameDict = request.POST
  	print(request.body.decode()) # 输出的是json字符串，如果直接输出request.body是二进制串
  
  	return HttpResponse('23')
  ```

  

### 静态资源

虽然现在使用前后端分离的方式开发，页面放到web目录中，静态资源放到cdn上。但是需要有cdn。如果没有cdn还是需要解决静态资源的问题。

#### 返回页面

要返回页面，首先需要配置html文件的路径，然后渲染出来。首先我们需要设置模板的查找路径。当我们创建应用时，系统默认的会设置APP_DIRS = True，然后我们可以在应用目录下新建template目录，然后就可以找到模板文件了。

__方式1__

设置应用模板路径

>project_name/settings.py(这里是mysite/settings.py)文件

```
TEMPLATES= [
	{
		....
		'APP_DIRS': True,
		....
	}
]
```

> > 注意！按照上面写不行，还需要在__INSTALLED_APPS__字段里添加我们创建的应用名字才可以。

```
INSTALLED_APPS = [
	...
	'polls', # polls是我们应用的名字
]
```

__方式2__

设置工程模板路径

> project_name/settings.py

```
TEMPLATES= [
	{
		'DIRS': [os.path.join(BASE_DIR, 'templates')], # 直接写绝对路径也可以
		....
		....
	}
]
```

> > 这是__INSTALLED_APPS__字段不添加应用名称也是可以的

这里只写如何能访问到模板，不会写太多模板



#### 返回静态资源

静态资源不包括模板文件，除此之外，有imge、css、js等，都是静态资源。在Django中这些资源是__static files__，所以关于这些资源的设置都会跟关键字__static__有关。

设置需要做如下steps

1. 添加__django.contrib.staticfiles__到__INSTALLED_APPS__中

> project_name/settings.py

```
INSTALLED_APPS = [
	...
	'django.contrib.staticfiles',
	...
]
```

2. 设置__STATIC_URL__路径

> project_name/settings.py

```
STATIC_URL = '/static/'
```

3. 在我们应用的模板文件中添加__static__标签来指定静态文件。

> 应用的任何模板文件(html文件)

```
{% load static %}
<img src="{% static "my_app/example.jpg" %}" alt="My image">
```

主要是 __static__标签的使用。还可以不用static标签，直接使用绝对路径来访问静态资源

```
<img src="/static/my_app/example.jpg" alt="My image">
```

写成上面方法是就可以访问了。

4. 在应用创建static目录

```
my_app/static/my_app.example.jpg
```

> 注意：这里也需要在__INSTALLED_APPS__加上我们的应用。

> > 说明：静态资源的访问方式类似于模板文件的配置，有应用中创建静态资源目录或者在工程下创建静态资源文件。

跟静态资源设置有三个字段：

STATIC_ROOT（None）：生产环境下所有静态资源的位置

> project_name/settings.py

```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

然后在命令行运行`python manage.py collectstatic`。Django会将所有的静态资源都放置到__STATIC_ROOT__目录下。

STATIC_URL（None）：不使用static标签时，指定的前缀路径

> project_name/settings.py

```
STATIC_URL = 'static'
```

在模板文件中可以使用绝对定位的方式访问静态资源。

STATICFILES_DIRS（[]）：额外静态资源的查找路径列表

> project_name/settings.py

```
STATICFILES_DIRS = [
	....
]
```

__线上部署__

1. 设置STATIC_ROOT
2. Run `python manage.py collectstatic  `命令，搜集静态文件
3. 开启静态资源服务器



### 数据库

后台服务在提供服务的时候一般都是跟具体的数据有关的，如果没有数据只是纯粹的逻辑是不现实的。即使是静态页面的内容一般也都需要数据，这些数据的来源一般是从数据库中读取到的。所以数据库操作是后台开发必不可少的内容。

#### 连接数据库

Django默认提供了orm的功能，我们使用默认的就可以了。但是还是需要连接数据库。连接相关的配置在工程配置文件中。

> project_name/settings.py，这里是mystie/settings.py文件

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

__ENGINE__：数据库引擎

`'django.db.backends.sqlite3'`，`'django.db.backends.postgresql'`，`'django.db.backends.mysql'`，或 `'django.db.backends.oracle'`。其它 [可用后端](https://docs.djangoproject.com/zh-hans/2.2/ref/databases/#third-party-notes)

__NAME__：数据库名称，如果是SQLite值是文件的绝对路径。

这里使用的SQLite数据库，如果不是，可能还需要一些额外配置：__USER__、__PASSWORD__和__HOST__等。具体查看相关文档。 

> SQLite之外的数据库连接，需要在连接前已经创建了相应的数据库。

#### 数据来源

数据库来源要么是从0开始构建，要么是从现有的数据库导入。这里我们分不同情况讨论。

1. __从0构建数据库__

Django的orm相关知识中，使用数据模型来描述数据。也就是数据库结构设计和附加的其它元数据。

定义数据模型

> app_name/models.py，这里是 polls/models.py文件

```
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

*一些models相关的知识，在具体使用时在学习。*

上面创建了数据模型，但是还没有创建相应的数据库。我们可以使用Django提供的migrate相关命令来做这件事。

> 说明：一般情况下，需要在__INSTALLED_APPS__中加入我们创建的应用，

> mysite/settings.py文件

```
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    ...
]
```

这里其实可以直接写'polls'就可以了。不需要写这么多

```
INSTALLED_APPS = [
		...
    'polls',
    ...
]
```

__激活模型__

可以使用`makemigrations`来根据models.py文件的__变化__来创建相应的数据库的修改操作。

```
python manage.py makemigrations polls[app_name]
```

执行之后就会创建一些迁移文件，我们可以直接查看相应的源码或者可以使用`sqlmigrate`命令来看具体做了什么。

```
python manage.py sqlmigrate app_name changed_index
python manage.py sqlmigrate polls 0001
```

__sqlmigrate__命令只是显示将要执行的命令，还没有创建具体的数据库，如果想实际执行，需要执行`migrates`命令。

```
python manage.py migrate [polls，app_name]
```

执行后就会创建相应的数据库结构。

> 总结下来就是两步（或者三步，包括查看相应sql语句）

1. `python manage.py makemigrations app_name`
2. `python manage.py sqlmigrate app_name changed_index`
3. `python manage.py migrate app_name`

__说明__

`migrate`命令还有其它的参数，比如说指定database等。使用时在查看。

2. __现有库导入__







### 配置文件