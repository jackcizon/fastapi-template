"""entry point for FastAPI APP"""

import uvicorn

from src.core.application.lifespan import lifespan
from src.core.config import settings
from src.core.application.lazy_load_app import LazyLoadApp

# app factory
# use `.instance` to get `app:FastAPI instance`
app = LazyLoadApp(debug=settings.debug, lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", factory=True, reload_dirs=["src"])
