# Security

生成jwt`key`, 不推荐使用`uuid`, 建议使用：

```python
import secrets

JWT_KEY = secrets.token_hex(32)
```
