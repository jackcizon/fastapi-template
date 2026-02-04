# Security and Test

## security

生成jwt`key`, 不推荐使用`uuid`, 建议使用：

```python
import secrets

JWT_KEY = secrets.token_hex(32)
```

## Test

必须测试：

```text
apps/*/service(mock)
apps/*/repo(集成测试sqlite)
apps/*/domain
apps/*/policy
utils/* 有 if 的
core/* 有判断逻辑的
auth / security
token
permission
```

可选测试：

```text
routes(unittest ignore, e2e需要测试)
exception handler
middleware
```

不用测试：

```text
config
db session
app init
logging setup
pure wrapper
```
