# ABOUTME: Test configuration ensuring backend package import paths resolve in pytest.
# ABOUTME: Injects repository backend root into sys.path for local test execution.
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
