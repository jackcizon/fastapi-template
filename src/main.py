"""entry point for FastAPI APP"""

from src.core.config import settings
from src.core.application.lazy_load_app import LazyLoadApp

app = LazyLoadApp(debug=settings.debug)
