# ABOUTME: Imports model metadata for table creation and migration awareness.
# ABOUTME: Ensures ORM models are registered before create_all execution.
from app.models import models  # noqa: F401
