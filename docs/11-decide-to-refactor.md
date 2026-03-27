# Decide To Refactor

When the responsibilities of different modules in a project become blurred, and functionality becomes redundant.

**Don't Repeat Yourself(DRY)**

it's crucial to start considering the correctness and maintainability of the project structure.

## Several points to consider during refactoring.

In `src`:

- kernel|core|common: Shared, core business logic

- utils: Business logic unrelated

- api: Various domains

In `src/core`:

- api: api related

- db: database related

- cli: command line interface

- services: common business

In `tests`:

- utils: Test utility-related code

- api: Test api-related code

In `utils/api`:

- routes: API tests
- services: Business logic tests
- repos: DB tests
-schemas: DTO tests
