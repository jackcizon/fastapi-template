# Feat Models

1. `sqlmodel` is no longer used; its functionality is too poor and it's completely inferior to `sqlalchemy`.

2. Unit testing and test coverage reporting for `models.py` will no longer be performed.

3. `FK` will not be set in the database; all relational semantics will only exist in `ORM`.

4. Deletes will default to `soft delete`.

5. All (cascading) deletes must be written only in the `Service` layer.

6. Deleted data will be uniformly filtered during queries.

7. Primary keys don't need to be considered in the current table (natural index), but once this primary key appears in "
   other tables" → as a logical foreign key → an index will be added by default.

8. If `FK` is disabled (essentially required), then the `x-x(x in [1, m, n])` relationship can only be guaranteed by the
   `Service` layer.

9. `index` is only for speed improvement, ensuring that when using code `service` to determine table relationships
   without using `FK`, the speed will not be slower.