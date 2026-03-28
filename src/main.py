"""entry point for FastAPI APP"""

import uvicorn

from src.core.config import settings
from src.core.application.lazy_load_app import LazyLoadApp, AppFactory

# app factory
# use `.instance` to get `app:FastAPI instance`
app = LazyLoadApp(debug=settings.debug)

if __name__ == "__main__":
    uvicorn.run(app=app, factory=True)
    # uvicorn.run(app=app(), factory=False)
