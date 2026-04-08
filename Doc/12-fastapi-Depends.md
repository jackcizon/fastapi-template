# FastAPI Depends

```python
from fastapi.dependencies.utils import solve_dependencies  # depends inner logic

@dataclass(frozen=True)
class Depends:
    dependency: Optional[Callable[..., Any]] = None
    use_cache: bool = True
    scope: Union[Literal["function", "request"], None] = None
```

`use_cache` will cause some bugs.

e.g.:

```python
class RolePermissionCheck:

    def __init__(self) -> None:
        self._user: User | None = None
        self._permission_code: str | None = None
        self._role: str | None = None
        self._passed: bool = False  # state

    def assign_args(self, request: Request, user: User) -> None:
        self._user = user
        route: APIRoute = request.scope.get("route")
        self._permission_code = route.name
        metadata: dict[Any, Any] | None = route.openapi_extra
        if metadata is None:
            self._role = DEFAULT_ROLE
        else:
            self._role = metadata.get("role")

    def _has_permission(self, db: Session, user: User) -> bool:
        user_permissions = RbacRepo(db).get_user_permissions(user)
        codes = [user_permission for user_permission in user_permissions]

        if self._permission_code in codes:
            self._passed = True
        return self._passed

    def _result(self) -> tuple[User, str]:
        return self._user, self._role

    def __call__(
            self,
            request: Request,
            db: Session = Depends(get_db),
            user: User = Depends(jwt_required_dep),
    ) -> tuple[User, str]:
        self.assign_args(request, user)
        if not self._has_permission(db, user):
            raise HTTPException(status_code=403, detail="403 Forbidden")
        return self._result()
```

## Bad solution:

use lock:

```python
def __call__(self):
    with self.lock:
        # process
        pass
```

State Pollution: FastAPI caches Depends instances. If you use `self._passed` as a container to store validation results,
under concurrent requests, B's "pass" will become A's "pass".

Rapid Probability:

Even if you add an `else` statement to reset the state, during the instant of asynchronous `await` switching, multiple
threads/coroutines will still overwrite data on `self`.

Incorrect Approach: Adding locks will cause a sharp performance drop and is meaningless.

Solution:

- Completely abandon storing request data in `self.xxx`.
- allowing data to flow on the **call stack**, not on `self.xxx` (Heap).
- write whole code in __call__(), make sure all code are in function `stack`.

## final solution:

### solution 1

use a func wrapper, each request create a new cls.

```python
async def role_prem_check_wrapper_dep(
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(jwt_required_dep)
):
    checker = RolePermissionCheck()
    return await checker(request, db, user)
```

### solution 2

use pure function: stateless

```python
def role_permission_check_dep(
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(jwt_required_dep),
) -> tuple[User, str]:
    """
    :return: tuple(user_instance, min_req_role_str)
    """
    route: APIRoute = request.scope.get("route")
    permission_code = route.name
    metadata: dict[Any, Any] | None = route.openapi_extra
    if metadata is None:
        role = DEFAULT_ROLE
    else:
        role = metadata.get("role")

    user_permissions = RbacRepo(db).get_user_permissions(user)
    codes = [user_perm for user_perm in user_permissions]
    if permission_code not in codes:
        raise HTTPException(status_code=403, detail="403 Forbidden")
    return user, role
```

## Note

Class attributes (self.xxx) = Heap memory or static global variables When you define a class instance and it is
cached by FastAPI, it's as if a space is malloced on the heap, or a global static struct is defined. All requests (
threads/coroutines) hold pointers to the same address. Function local variables $\approx$ Stack memory When
role_permission_check_dep is called, it's as if a function is entered in C. The system pushes a stack frame onto the top
of the current thread's stack.

Stack memory is created when a function is called and destroyed when the function returns, physically isolating
requests.