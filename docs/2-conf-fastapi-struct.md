# Conf FastAPI Struct

1. 不能再使用`url.py` + `views.py`, 这是反模式, 使用`routes.py`
2. 不再需要app启动和总`urls.p`分离, 直接在app实例化后添加路由表
3. 启动时在pycharm的配置中，设置启动目录在`main.py`所在目录，并设置
   `PYTHONPATH=src`, 这样就不用写`src`了
4. 启动时要以`module`级别启动module`uvicorn`, `parameters`中填写
   相关的启动参数(详情见`uvicorn --help`)
5. `3`在django，这种框架下工作是可行的，但这仍然需要insert into `sys.path`,
   显然不符合fastapi的原则，在fastapi中，直接从`src`导包即可，否则后续测试等
   都会遇到问题(因为pip包的导入原则)