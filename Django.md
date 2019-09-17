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

__从0构建数据库__

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

Django默认使用的数据库是sqlite，但很多公司会使用mysql等数据库，所以还需要测试一下怎么连接mysql。

##### 连接MySQL

连接MySQL的操作跟sqlite有很大的区别。连接sqlite数据库时，`NAME`字段对应的是sqlite数据库的文件地址。而mysql是相应的数据的名字。所以我们需要先创建相应的数据库。然后在进行相应的数据库迁移。

__连接配置__

>project_name/settings.py，这里project_name是mysite

```
DATABASES = {
	# 'default': {
	#     'ENGINE': 'django.db.backends.sqlite3',
	#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	# }
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'soda', # 数据库名称
		'USER': 'root', # 数据库登录用户
		'PASSWORD': 'password', # 数据库登录密码
		'HOST': '127.0.0.1', # 数据库地址
		'PORT': '3306', # 端口
	}
}
```

做好后，我们可以使用__inspectdb__命令来查看数据库结构。

```
python manage.py inspectdb > polls/models.py
```

运行上面命令后，会创建相应的models文件。我们可以通过__shell__命令来查看是否入成功了。

`inspectdb`命令只是根据数据库结构来创建models文件，但是还没有进行迁移数据。迁移数据还是需要migrate命令。但是命令需要加上``--fake-initial``选项。

```
python manage.py migrate --fake-initial
```

> 说明：加上`--fake-initial`选项，是为了应对数据库里已经有数据时不会报错，同时不会修改原来的数据库。因为__migrate__命令会在没有数据库结构根据models.py文件来创建相应的数据库。但是如果有了就不需要创建了。



---

在连接数据库时报错了，说是连接引擎不对，尝试了一些方法没有成功，最后就将Django的版本固定到了2.1。然后就成功了。

安装pymysql：

```
pip install pymysql -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

安装文件后，还需要做一些配置

> project_name/init.py，这里是mysite/init.py文件

```
import pymysql

pymysql.install_as_MySQLdb()
```

安装2.1版本的django

```
pip install django==2.1
```

#### 多数据库连接

一个服务可能同时连接多个数据库，有时一个应用也可以同时连接多个数据库。所以连接多个数据库也是其中的一种情况。

1. 首先我们需要在settings.py文件中添加数据库连接配置

> project_name/settings.py文件，这里project_name的值是mysite

```
...
DATABASES = {
	'default': {
	    'ENGINE': 'django.db.backends.sqlite3',
	    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	},
	'soda': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'soda',
		'USER': 'root',
		'PASSWORD': 'password',
		'HOST': '127.0.0.1',
		'PORT': '3306',
	}
}
...
```

如上所示，在`DATABASES`字段添加了新的数据库连接配置。

2. 然后需要创建数据库和app的对应的映射关系

> project_name/setttins.py文件，这里project_name的值是mysite

```
DATABASES_APPS_MAPPING = {
	# 'app_name': 'database_name'
	'storage': 'defalut',
	'polls': 'soda',
}
```

>>key是app_name，value是数据库 

3. 还需要创建数据库路由规则：DATABASE_ROUTERS

> project_name/settings.py文件，project_name是mysite

```
DATABASE_ROUTERS = ['project_name.database_router.DatabaseAppsRouter']
这里是：
	DATABASE_ROUTERS = ['mysite.database_router.DatabaseAppsRouter']
```

然后在相应的文件里定义相关的函数`db_for_read`、 `db_for_write`、 `allow_relation`、 `allow_migrate`，在这些函数里定义如何处理应用和数据库的关联。

> mysite/database_router.py文件，其中mysite是project_name的值

```
from django.conf import settings


DATABASES_APPS_MAPPING = settings.DATABASES_APPS_MAPPING

class DatabaseAppsRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label in DATABASES_APPS_MAPPING:
			return DATABASES_APPS_MAPPING[model._meta.app_label]
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label in DATABASES_APPS_MAPPING:
			return DATABASES_APPS_MAPPING[model._meta.app_label]
		return None

	def allow_relation(self, obj1, obj2, **hints):
		db_obj1 = DATABASES_APPS_MAPPING.get(obj1._meta.app_label)
		db_obj2 = DATABASES_APPS_MAPPING.get(obj2._meta.app_label)

		if db_obj1 and db_obj2:
			if db_obj1 == db_obj2:
				return True
			else:
				return False
		return None

	def allow_syncdb(self, db, model):
		if db in DATABASES_APPS_MAPPING.values():
			return DATABASES_APPS_MAPPING.get(model._meta.app_label) == db
		elif model._meta.app_label in DATABASES_APPS_MAPPING:
			return False
		return None

	def allow_migrate(self, db, app_label, model=None, **hints):
		if db in DATABASES_APPS_MAPPING.values():
			return DATABASES_APPS_MAPPING.get(app_label) == db
		elif app_label in DATABASES_APPS_MAPPING
			return False
		return None

```

这里models的_meta属性中的app_label需要我们在相应的models中设置。比如说：

```
DATABASES_APPS_MAPPING = {
	# 'app_name': 'database_name'
	'storage': 'defalut',
	'polls': 'soda',
}
```

这里的app_name是storage，所以需要storage应用内的models.py文件中的模型meta属性中的app_label的值是storage。

```
class Question(models.Model):
	question_text = models.CharField(max_length=200)

	def __str__(self):
		return self.question_text

	class Meta:
		app_label = 'storage'
```

经过上面的操作，数据库和应用就可以绑定在一起了。

#### 数据库操作

单数据库操作时可以按照官方文档上的操作来做。当是多数据库时，在操作时需要指定具体的数据。

比如说上面我们设定的多数据库连接的storage数据库。从storage数据中引入了User表，然后使用时是

```
User.objects.using('storage').all()
```

必需要加上`using('storage')`操作才是真正的操作数据库。



### 缓存

当网站访问量比较少时，无所谓。但是当网站访问量比较大时就需要缓存了。比如说渲染页面。访问量比较大时，如果没有缓存，每次请求都会访问数据库，导致数据库压力大。但是如果对于访问过的页面进行缓存，就可以减少这样的压力。

```
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache (for next time)
    return the generated page
```

缓存可以存放于数据库、文件系统，或者直接放在内存（一般推荐）很影响性能。

常用的缓存工具。

#### Memcached

是一个基于内存的缓存服务器。有两种绑定：`python-memcached`和`pylibmc`。可以自行决定使用哪一种绑定。

选择好之后，在配置文件中进行相关的设置。

> /mysite/settings.py

```
CACHES = {
	'defalut': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}
```

- BACKEND：django.core.cache.backends.memcached.MemcachedCache或者django.core.cache.backends.memcached.PyLibMCCache
- LOCATION：
    - ip:port。其中ip是memcached守护进程的IP地址，port是memcached守护进程监听的端口；
    - unix:path。其中path是Memcached Unix套接字文件的路径。

比如使用`python-memcached`绑定，在localhost(127.0.0.1)端口11211上运行：

```
CACHES = {
	'defalut': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}
```

Memcached可通过本地Unix套接字文件`/tmp/memcached.sock`使用python-memcached绑定：

```
CACHES = {
	'defalut': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': 'unix:/tmp/memcached.sock',
	}
}
```

当使用`pylibmc`时，可以省略`unix:/`前缀。

基于内存的缓存有一个缺点，就是服务器崩溃时，缓存的数据就失效了。

#### 数据库缓存

需要将配置文件中的BACKEND修改一下

> mysite/settings.py

```
CACHES = {
 `   'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```

- **BACKEND**设置为`django.core.cache.backends.db.DatabaseCache`
- **LOCATION**：设置为 数据库表的``表名``。比如上面的`my_cache_table`

**创建缓存表**

使用数据库缓存钱，必须先创建缓存表

```
python manage.py createcachetable
```

**多数据库**

需要配置一下路由。



#### 文件系统缓存

需要将BACKEND设置为`django.core.cache.backends.filebased.FileBasedCache`，并将LOCATION设置为一个合适的路径。

> mysite/settings.py

```
# *nix系统
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
```

```
# windows系统
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'c:/foo/bar',
    }
}
```

配置好之后需要确保LOCATION指向的路径是可以访问的。

**本地内存缓存**

```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

**虚拟缓存(用于开发模式)**

```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
```



#### Redis缓存

Django自身并没有带redis缓存，需要我们安装相应的软件：`django-redis`

```
pip install django-redis
```

工程配置文件

> mysite/settings.py

```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```





**缓存参数**

- **TIMEOUT**：缓存超时时间(单位秒)，默认300s

- **OPTIONS**：

    - **MAX_ENTRIES**：缓存最大个数
    - **CULL_FREQUENCY**：当**CULL_FREQUENCY**达到最大条目时，需要淘汰的条目数。实际比率为`1/CULL_FREQUENCY`，比如说CULL_FREQUENCY=2时，有一半会被删除。

- **KEY_PREFIX**：将自动包含到Django服务器使用的所有缓存键的字符串

- **VERSION**：缓存键的默认版本号

- **KEY_FUNCTION**：

    这个例子中，文件系统被设置成60秒超时时间，最大容量为1000条

    ```
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }
    ```

    使用python-memcached后端，大小限制在

**站点缓存**

**视图缓存**

**模板片段缓存**

**底层缓存API**

- **访问缓存**

    **django.core.cache.caches**

    可以通过类似字典一样的object：**django.core.cache.caches**对象访问在`CACHE`配置的缓存。类似于数据库的配置。

    ```
    from django.core.cache import caches
    ```

    **django.core.cache.cache**

    作为快捷方式，默认缓存可以通过**django.core.cache.cache**引用：

    ```
    from django.core.cache import cache
    ```

    这个对象等价于**caches['default']**。

- **基本用法**

    **cache.set**(key, value, timeout=DEFAULT_TIMEOUT, version=None)

    ```
    cache.set('my_key', 'hello', 30)
    ```

    **cache.get**(key, default=None, version=None)

    ```
    cache.get('my_key')
    ```

    **key**是一个字符串，value可以是任何picklable形式的Python对象

    如果对象不再缓存中，**cache.get()**将返回**None**。

    `cache.get()`可以带一个默认参数。如果对象不在缓存中，将返回指定的值。

    ```
    cache.get('my_key', 'has expired')
    # 如果my_key不存在，将返回has expired
    ```

    **cache.add**(key, value, timeout=DEFAULT_TIMEOUT, version=None)

    于set类似。如果键不存在则添加，键存在不更新。

    **cache.get_or_set**(key, default, timeout=DEFAULT_TIMEOUT, version=None)

    有键返回，无键则设置新的值

    **cache.get_many**(keys, version=None)

    返回一个字典。这些键真实存在缓存中（并且没过期）

    **cache.set_many**(dict, timeout)

    传递多个键值对来设置缓存

    **cache.delete**(key, version=None)

    删除某个键

    **cache.delete_many**(keys, version=None)

    一次删除多个键。参数是key的列表

    **cache.clear**()

    清除所有的key

    **cache.touch**(key, timeout=DEFAULT_TIMEOUT, version=None)

    更新过期时间

    如果更新成功，返回True，否则反水False。

    **cache.incr**(key, delta=1, version=None)：自增key

    **cache.decr**(key, delta=1, version=None)：自减key

    **cache.close**()：2.1版本之后新加的

    如果缓存后端实现了`close()`方法，可以关闭和缓存的连接。





### 日志

 

### 配置文件



### 项目依赖

1. 虚拟环境

    当在`virtualenv`环境下时，我们可以使用`pip freeze > requirements.txt`命令来生成依赖文件。

2. 扫描项目

    我们并不一定永远都是在有虚拟环境下工作的，所以虚拟环境具有一定的要求。可以使用`pipreqs`来解决这样的问题。

    > 安装pipreqs

    ```
    pip install pipreqs
    ```

    > 创建依赖文件

    ```
    pipreqs . // 点是工程路径
    ```

    上面中的[**.**]是工程的路径，如果不是在工程下，需要指定后面就需要指定工程的路径了。

3. 安装依赖

    ```
    pip install -r /django_project_path/requriements.txt 
    ```

    

### 相关问题

1. sqlite3版本问题

    python一般会自带sqlite3。但是这个可能跟django要求的sqlite3版本不一致，从而导致问题。

    先查看当前python版本使用的sqlite3版本

    ```
    python
    >>>import sqlite3
    >>>sqlite3.sqlite_version
    ```

    运行上面命令就可以看到当前python使用的sqlite3的版本了。

    django 2.2及以后的版本要求sqlite3 > 3.8.3，但是python自带的只有3.7.3。所以我们需要安装新版本的sqlite3。

### 线上部署

开发好之后就需要部署上线了。但是部署时就不能仅仅使用`python manage.py runserver`命令。这个命令只适用于在本地开发时使用。

WSGI是一种协议，一边连接着服务器，一边连接着Django应用。这样能很好的做到扩展。比如说同一个上游代理，后面可以跑很多个应用。只要这个应用实现了WSGI协议就可以。

Django在开发时，会自动开启一个WSGI服务器，但是性能不好。在线上会有问题。但是有一些专门的工具来做这件事。

**uWSGI**、**gunicorn** 和 **bjoern** 都是实现了`uwsgi`、`wsgi`、`http`等协议的工具。尤以uWSGI使用比较广。uWSGI是一个实现了一些协议的服务器软件。一边连着web服务，一边连着Python开发的应用。

**uWSGI**

uWSGI是一个实现了uwsgi和WSGI协议的软件。可以通过命令行的方式启动，也可以通过启动文件来启动。但是都需要做一些相关配置

- chdir=// # 指定Python项目目录
- home= # 指定虚拟机环境
- wsgi-file= # 加载WSGI文件
- socket= 指定uwsgi的客户端将要连接的socket的路径（使用UNIX socket的情况）或者地址（使用网络地址的情况）。
- callable= # uWSGI加载的模块中哪个变量将被调用
- master=true/false # 指定启动主进程
- processes # 设置工作进程的数量
- threads # 设置每个工作进程的线程数
- vacuum=true # 当服务器退出时自动删除unix socket文件和pid文件
- logfile-chmod=644 # 指定日志文件的权限
- daemonize=%(chdir)/xxx.log # 进程在后台运行，并将日志打印到指定文件
- pidfile=%(chdir)/xxx.pid # 在失去权限前，将主进程pid写到指定的文件
- uid=xxx # uWSGI服务器运行时的用户id
- gid=xxx # uWSGI服务器运行时的用户组id
- Procname-prefix-spaced=xxx # 指定工作进程名称的前缀

> django_uwsgi.ini文件示例

```
[uwsgi]
chdir=/home/git/www/cloudmonitor # 指定项目目录
home=/home/git/www/cloudmonitor/.env # 指定python虚拟环境
wsgi-file=manager.py # 指定加载的WSGI文件
callable=app # 指定uWSGI加载的模块中哪个变量将被调用
master=true # 启动主线程
processes=4 # 设置工作进程的数量
threads=2 # 设置每个工作进程的线程数
socket=127.0.0.1:8888 # 指定socket地址
vacuum=true # 当服务器退出时自动删除unix socket文件和pid文件
logfile-chmod=644 # 指定日志文件的权限
daemonize=%(chdir)/cloudmonitor.log # 进程在后台运行，并将日志打印到指定文件
pidfile=%(chdir)/cloudmonitor.pid # 在失去权限前，将主进程pid写到指定的文件
uid=git # uWSGI服务器运行时的用户id
gid=git # uWSGI服务器运行时的用户组id
procname-prefix-spaced=cloudmonitor # 指定工作进程名称的前缀
```

如果是socket启动，在配置nginx时，也同样是启动socket端口。如果是http方式启动，nginx配置是也需要http方式启动。





### 参考

[Django + uWSGI + Nginx详解](https://www.jianshu.com/p/1c50b15b143a)

