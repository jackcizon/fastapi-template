# About Django to FastAPI

## Rewriting from Django + DRF to FastAPI, the most difficult part is almost always the DB layer (ORM + ecosystem)

And when you switch to FastAPI:

- No default ORM (you have to choose one yourself)
- No migrations (you have to integrate with Alembic yourself)
- No admin (you have to create it yourself or give up)
- Data validation and ORM are separate (Pydantic vs ORM)

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

- No foreign keys required
- Only *_id in the DB layer
- High performance (avoids N+1 constraints)
- Can be used in distributed systems (does not depend on DB constraints)
