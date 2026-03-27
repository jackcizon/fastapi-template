"""entry point for FastAPI APP"""

from src.core.config import settings
from src.core.application.lazy_load_app import LazyLoadApp

# app factory
# use `.instance` to get `app:FastAPI instance`
app = LazyLoadApp(debug=settings.debug)
