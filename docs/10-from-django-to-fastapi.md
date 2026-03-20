# About Django to FastAPI

## Rewriting from Django + DRF to FastAPI, the most difficult part is almost always the DB layer (ORM + ecosystem)

And when you switch to FastAPI:

- No default ORM (you have to choose one yourself)

- No migrations (you have to integrate with Alembic yourself)

- No admin (you have to create it yourself or give up)

- Data validation and ORM are separate (Pydantic vs ORM)

Essentially, you have to do the architecture design yourself.

This is the normal stage:

Proficient in Django → Fast

Early stages of FastAPI → Slow + Tiring

This is changing the "abstraction level"

## Implementing the "Same Design" with Two Frameworks

The core is: Aligning the abstraction layers

Define a "unified domain model" first (don't write code first)

Required: The first version should be entirely synchronous (sync SQLAlchemy)

Only switch to async after you get it working.

If you really want to "brute force + high returns," you can upgrade to:

Single database + Dual Backends

Structure:

PostgreSQL

├── Django API

└── FastAPI API

Advantages:

Completely consistent data

Performance comparisons possible

Development experience comparisons possible

## Optimal Path:

Unified Domain Model (Design First)

Dual Implementation (Feature-by-Feature)

Completely consistent DB structure

FastAPI initially uses sync + SQLAlchemy

No optimization, no refactoring, just get it running.

## You're Switching from "Declarative Development" to "Explicit Architecture Design"

Feeling tired, slow, and needing to think for a long time—this isn't regression; it's you moving away from Django's "
autopilot."

In FastAPI + SQLAlchemy:

Essentially:

You're "implementing every layer by hand."

II. The Real Reason You "Need to Think for a Long Time" Now

It's not that you're slow, but that you're dealing with these issues (Django hides them for you):

### Data Flow Design (Most Mentally taxing)

You need to think about:

Request -> Schema -> ORM -> DB -> ORM -> Schema -> Response

While DRF:

Serializer handles everything at once.

### Boundary Delineation (This is an Advanced Skill)

Don't just write code; you must "summarize and abstract."

## Example: A reasonable SQLAlchemy for 1-1, 1-n, n-n: declaration, foreign keys prohibited, DB layer must use *_id,

## only allowed in ORM layer, high performance, and distributed capability.

✔ No foreign keys required

✔ Only *_id in the DB layer

✔ Relationships declared only in the ORM layer

✔ High performance (avoids N+1 constraints)

✔ Can be used in distributed systems (does not depend on DB constraints)

I'm not giving you a "tutorial version," only a practical implementation.

### First, establish a general principle (very crucial)

In SQLAlchemy:

relationship = query descriptor, not constraint

Therefore, we use:

primaryjoin

foreign() (crucial!)

selectin (performance critical)

#### 1-1 (One-to-One)

Scenario: User ↔ Profile

profile.user_id

Writing (no foreign key version)

```python
from sqlalchemy.orm import relationship, foreign


class User(Base):
    __tablename__ = "user"
    id = mapped_column(primary_key=True)
    profile = relationship(
        "Profile",
        primaryjoin="User.id == foreign(Profile.user_id)",
        uselist=False,  # Crucial: 1-1
        lazy="selectin"
    )


class Profile(Base):
    __tablename__ = "profile"
    id = mapped_column(primary_key=True)
    user_id = mapped_column(index=True)

    user = relationship(
        "User",
        primaryjoin="foreign(Profile.user_id) == User.id",
        lazy="selectin"
    )
```

Key points: uselist=False → Controls 1-1

foreign() → Tells the ORM which side is the "foreign key role"

No need for ForeignKey

#### 1-N (One-to-Many)

Scenario: User → Orders

orders.user_id

```python

class User(Base):


__tablename__ = "user"

id = mapped_column(primary_key=True)

orders = relationship(
    "Order",

    primaryjoin="User.id == foreign(Order.user_id)",

    lazy="selectin"

)


class Order(Base):


__tablename__ = "order"

id = mapped_column(primary_key=True)

user_id = mapped_column(index=True)

user = relationship(
    "User",

    primaryjoin="foreign(Order.user_id) == User.id",

    lazy="selectin"

)
```

High-performance usage (important)

select(User).options(selectinload(User.orders))

Becomes:

1 user, 1 orders (IN query), avoiding N+1

#### N-N (Many-to-Many, RBAC core)

Scenario User ↔ Role ↔ Permission
Intermediate table: User2Role Role2Permission
Writing method (no foreign key + manual join) User ↔ Role

```python

class User(Base):


__tablename__ = "user"

id = mapped_column(primary_key=True)

roles = relationship(
    "Role", secondary="user2role",
    primaryjoin="User.id == foreign(User2Role.user_id)",
    secondaryjoin="Role.id == foreign(User2Role.role_id)",
    lazy="selectin"
)


class Role(Base):
    __tablename__ = "role"


id = mapped_column(primary_key=True)

users = relationship(
    "User",
    secondary="user2role",
    primaryjoin="Role.id == foreign(User2Role.role_id)",
    secondaryjoin="User.id == foreign(User2Role.user_id)",
    lazy="selectin"
)


# Role ↔ Permission


class Role(Base):
    ...
    permissions = relationship(
        "Permission",
        secondary="role2permission",
        primaryjoin="Role.id == foreign(Role2Permission.role_id)",
        secondaryjoin="Permission.id == foreign(Role2Permission.permission_id)",

        lazy="selectin"

    )


class Permission(Base):
    __tablename__ = "permission"
    id = mapped_column(primary_key=True)
    roles = relationship(
        "Role",
        secondary="role2permission",
        primaryjoin="Permission.id == foreign(Role2Permission.permission_id)",
        secondaryjoin="Role.id == foreign(Role2Permission_id)",
        lazy="selectin"

    )
```

### Performance Key Points

These 3 points must be done

Use selectinload

from sqlalchemy.orm import selectinload

stmt = select(User).options(
selectinload(User.roles)

.selectinload(Role.permissions)

Execution:

user
roles (IN)

permissions (IN)

It will not become a 4-table join

All *_id must have an index

user_id = mapped_column(index=True)

Always use lazy="selectin"

#### VI. Why this solution is suitable for "distributed" environments

The point you raised is actually quite advanced, let me explain:

Benefits of not using foreign keys

- Cross-database (sharding)

- Non-blocking writes

- No reliance on strong DB consistency

- Achieve eventual consistency

- ORM relationships still hold

Because:

ORM only cares about "how to query", not "constraints"

### Final form of the solution

Data layer

- *_id No foreign key
- High-performance SQL

ORM layer

- relationship (manual join)
- selectinload (avoid N+1)

User layer

- user.roles
- role.permissions