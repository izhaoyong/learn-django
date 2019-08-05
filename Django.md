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
python manager.py runserver --host HOST(0.0.0.0) --port PORT(8000)
```

其中HOST是ip地址，默认是本地可访问，如果想所有机器可访问可以写成__0.0.0.0__

PORT是服务监听的端口。

