# Security and Test

## security

When generating a JWT key, using `uuid` is not recommended; it is suggested to use:

```python
import secrets

JWT_KEY = secrets.token_hex(32)
```

## Test

Test required:

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

Optional tests:

```text
routes(unittest ignore, e2e需要测试)
exception handler
middleware
```

No testing required:

```text
config
db session
app init
logging setup
pure wrapper
```
