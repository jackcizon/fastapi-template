# ORM things

## !avoid db constraints

```python
user_id = Column(Integer, ForeignKey("user.id"))
```

This leads to database-level foreign key constraints and a host of problems.

It creates foreign keys in the database table, which is extremely inefficient.

Avoid doing this in your projects 100%! Otherwise, the project will crash as it grows, making debugging, optimization,
and modifications extremely difficult.

Even if you define something like this in your ORM:

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

`on_delete, etc...`, It doesn't have much effect; the limitations are still quite significant.

## use logic fk

In SQLAlchemy's standard practice:

Completely disable the use of `FK` and use `relationship()` instead.

```python
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    user = relationship(
        "User",
        primaryjoin="Post.user_id == User.id",
        foreign_keys=[user_id],
    )
```

You can get `user.id` from `post.user`.

In Django:

1. You can use `FK` as usual.

2. You must add `db_constraint=False`. Django handles logical foreign keys at the ORM layer, and `FK` will not appear at
   the database layer.

This is the biggest convenience that ORM provides for us.

Mapping between Django and SQLAlchemy:

| Django             | SQLAlchemy                              |
|--------------------|-----------------------------------------|
| `ForeignKey(User)` | `relationship("User", primaryjoin=...)` |
| `user_id`          | `Column(Integer)`                       |
| `related_name`     | `back_populates`                        |
| `select_related`   | `lazy="joined"`                         |
| `prefetch_related` | `selectinload()`                        |

## Using a layered structure to uniformly handle each table and its related tables

1. The `crud/repo` layer handles SQL tables and their relationships; 100% of the SQL code resides here.

2. The `service` layer handles business logic; SQL code is prohibited in this layer.

3. Use `soft delete` to quickly process SQL deletion logic.

4. Use `index` to index `id`; otherwise, relying solely on `service` and `crud` for full `joins` will only slow things
   down.

Delete user:

```python
def delete_user(user_id: int):
    session.query(User)
    .filter(User.id == user_id)
    .update({"is_deleted": True})
```

When a user is deleted, the table associated with them may also need to be deleted, depending on the situation.

Correct practice:

```python
# user_repo.py
def delete_user(user_id: int):
    session.query(Post).filter(Post.user_id == user_id).delete()
    session.query(Comment).filter(Comment.user_id == user_id).delete()
    session.query(User).filter(User.id == user_id).delete()


# user_service.py
def del_user(user_id):
    repo.delete_user(user_id)


# or by cls
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
        if not UserRepo.exists(session, user_id):
            raise ValueError("user not found")

        UserRepo.soft_delete(session, user_id)
        PostRepo.soft_delete_by_user(session, user_id)


def delete_user_handler(user_id: int):
    with session_scope() as session:
        UserService.delete_user(session, user_id)
```

While ORMs do have built-in `on_*(delete, update, etc...)`, this one-size-fits-all approach isn't ideal for high
concurrency.

Although `service` statements can dynamically handle code logic, their complexity is higher than ORM's automatic
processing.

However, ORM's `on_*` statements become ineffective when dealing with `SQL (scripts)` because there's no framework
environment for it.
