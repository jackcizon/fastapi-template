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
api/*/services(mock)
api/*/repos(integration test with sqlite)
api/*/schemas
api/*/routes
```

Optional tests:

```text
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
