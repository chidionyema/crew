# Standard: scheduling row, docs/reference/STANDARDS.md -- one scheduler, idp/scheduler; this is a code location it loads
# Rejected: a cron or a standalone `dagster dev` -- a second scheduler; the freshness policies must live where the one daemon evaluates them
"""The package lives beside tests/, not on the repo path; pytest runs from the repo root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
