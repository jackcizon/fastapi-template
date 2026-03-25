# Decide To Refactor

When the responsibilities of different modules in a project become blurred, and functionality becomes redundant (RY),

it's crucial to start considering the correctness and maintainability of the project structure.

## Several points to consider during refactoring.

In `src`:

- kernel|core|common: Shared, core business logic

- utils: Business logic unrelated

- apps: Various domains

In `src/core`:

- app: app related

- db: database related

- cli: command line interface

- services: common business

In `tests`:

- utils: Test utility-related code

- apps: Test app-related code

In `utils/apps`:

- routes: API tests

- services: Business logic tests

- repos: DB tests