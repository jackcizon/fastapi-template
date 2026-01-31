# Start Project

`fastapi`项目不需要像django那样准备程序入口文件`manage.py`,

`manage.py`为django程序设置了`ENV`, 而`fastapi`由`uvicorn`

这个入口启动, 因此只需要在项目真正入口写`main.py`去编写`app`实例.
