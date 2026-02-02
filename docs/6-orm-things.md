# ORM things

## !避免 db constraints

```python
user_id = Column(Integer, ForeignKey("user.id"))
```

这会导致数据库级别的外键约束，一堆问题。

它会在数据库表中创建外键，非常差劲。

100% 避免在项目中这么做，否则后面项目大了直接崩了，非常难调试优化，做修改。

即使在ORM中定义了类似：

```python
user_id = Column(
    Integer,
    ForeignKey(
        "user.id",
        ondelete="CASCADE",
        onupdate="RESTRICT"
    )
)
```

的`on_delete, etc...`, 也没什么大的作用，该受限制还是一点不少。

## 使用逻辑外键

在`sqlalchemy`的标准做法：

全面禁止使用`FK`，使用`relationship()`

```python
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)  # 普通字段, 不再标注FK
    user = relationship(
        "User",
        primaryjoin="Post.user_id == User.id",
        foreign_keys=[user_id],
        # viewonly=True,   # 关键！(这将处于只读模式， 不能改变user.id)
    )
```

通过`post.user`得到`user.id`

而`django`中：

1. 照常使用`FK`
2. 必须添加`db_constraint=False`，django在ORM层处理了逻辑外键，而DB层不会出现`FK`

这是ORM为我们做的最大便利。

django和sqlalchemy的映射：

| Django             | SQLAlchemy                              |
|--------------------|-----------------------------------------|
| `ForeignKey(User)` | `relationship("User", primaryjoin=...)` |
| `user_id`          | `Column(Integer)`                       |
| `related_name`     | `back_populates`                        |
| `select_related`   | `lazy="joined"`                         |
| `prefetch_related` | `selectinload()`                        |

## 使用分层结构，统一处理每个表及其关联表

1. `crud/repo`层处理sql表，及其关联关系，sql代码100%存在于此
2. `service`层处理业务代码，禁止在该层出现sql代码
3. 配合`soft delete`，快速处理sql的删除逻辑
4. 必须使用`index`索引`全部id`,否则仅靠service和crud是全盘`join`速度只会更慢。

删除user:

```python
def delete_user(user_id: int):
    session.query(User)
    .filter(User.id == user_id)
    .update({"is_deleted": True})
```

当user被删除，与其关联的表`可能要被删除`，看情况。

❌错误做法:

```python
# 各种地方 scattered
delete
from post where

user_id = x
delete
from comment where

user_id = x
delete
from like where

user_id = x
```

✔正确做法：

```python
# 以函数举例是为了简单起见

# user_repo.py
def delete_user(user_id: int):
    session.query(Post).filter(Post.user_id == user_id).delete()
    session.query(Comment).filter(Comment.user_id == user_id).delete()
    session.query(User).filter(User.id == user_id).delete()


# user_service.py
def del_user(user_id):
    repo.delete_user(user_id)


# or 通过cls
class UserRepo:

    @staticmethod
    def soft_delete(session, user_id: int):
        return (
            session.query(User)
            .filter(User.id == user_id)
            .update({"is_deleted": True})
        )

    @staticmethod
    def exists(session, user_id: int) -> bool:
        return session.query(
            session.query(User.id)
            .filter(
                User.id == user_id,
                User.is_deleted == False,
            )
            .exists()
        ).scalar()


class UserService:

    @staticmethod
    def delete_user(session, user_id: int):
        # 业务校验
        if not UserRepo.exists(session, user_id):
            raise ValueError("user not found")

        # 事务内编排
        UserRepo.soft_delete(session, user_id)
        PostRepo.soft_delete_by_user(session, user_id)


def delete_user_handler(user_id: int):
    with session_scope() as session:
        UserService.delete_user(session, user_id)
```

当然ORM也内置了`on_*(delete, update, etc...)`,但一劳永逸的做法对高并发并不好。

虽然`service`可以动态处理代码逻辑，但复杂度要比ORM自动处理高。

但ORM的`on_*`在面对`SQL(脚本)`就失效了，因为没有框架环境。
