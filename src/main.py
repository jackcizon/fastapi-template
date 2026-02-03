"""entry point for FastAPI APP"""

from src.utils.lazy_load_app import create_app

app = create_app()
