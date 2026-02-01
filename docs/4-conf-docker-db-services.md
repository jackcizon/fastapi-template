# Conf Docker DB Services

1. `docker`中的`container`必须监听`0.0.0.0`(开发阶段?),在`docker-desktop`
   环境下,访问`windows wireless LAN`中的`IPV4`地址。
2. wsl的防火墙相关端口必须开放，否则连接失败.
3. 在各种db tools的gui上远程连接，输入相应的账号密码，IP就是`1`中的`IP`.
4. 编写相关`services`时,使用`.env.*(dev/prod)`中的配置连接,避免暴露信息。
   连接方式帮助详见`scripts/`,或使用`docker compose --help`.
5. 使用db services必须设置`voulme`映射，否则数据不能持久化，每次`down`都会删除.
6. `python service`可以先不在本地`dev`阶段使用,部署时保证`service`一致即可.
7. 基本不需要`migrations`,除非是教育目的，事前都由`DBA`审核sql表,
   开发人员禁止擅自migrations，当然migrations就没什么意义.