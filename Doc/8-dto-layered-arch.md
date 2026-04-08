## DTO Layered Arch

The reason for using `schema` is that it's the only tool capable of validating input data (such as Web JSON).

However, some old frameworks incorrectly call it a `serializer`.

A `serializer` is far more complex than a `validator`; it includes methods like `create()` and `destroy()`, and it mixes
business logic with validation logic.

As projects grow, the code becomes extremely messy.

Therefore, a `data validator` is essentially a `schema` that only validates the incoming data, typically Web JSON.

`schema` is `DTO`(Data Transfer Object), the medium between JSON and service code.
input JSON -> DTO -> service

## service with repo
if service logic catch a exception, just raise a custom exception, its root cls must be `Exception`

then register some global exception handlers in `Fastapi` instance.

a repo must write in the app that defined the repo's model.

a service can invoke other app's repo.

if a service(DemoService) is complex, typically need 3-5 tables, then write a repo(DemoRepo) in this app is good,
then this repo do complex query, service just use this repo.

a model -> repo(recommend).

a service(simple) -> init a repo in __init__().

a service(complex) -> do not init repo(s), use different repos in service functions.

## arch

```text
Pydantic DTO
↓
Service (business logic)
↓
Repository (SQL)
↓
Database
```