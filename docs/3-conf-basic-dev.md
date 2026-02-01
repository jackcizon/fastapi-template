# Conf Basic Dev

1. `settings`/`config` 模块的配置必须通过`.env`导入，
   通过设置环境变量`ENV`=`dev`/`prod`，动态读取`.env`
2. fastapi的`settings cls`是常量集合, 可以自己设置cls，
   也可以用三方包，但是不能写继承关系.
3. 通过模块级别的单例类导出配置，要求配置必须与app隔离，按需导入
4. 每个app的`py files`必须职责明确，`tests`下直接复制`apps`的
   结构，再加`test_`前缀，方便测试和管理.
