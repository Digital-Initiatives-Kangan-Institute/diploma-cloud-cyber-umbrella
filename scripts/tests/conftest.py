"""Put the minimal test brand pack on sys.path so the course-agnostic engine tests need no real course.

The engine's helpers import `from brand import …`; a real course supplies brand.py in its content repo.
For the umbrella's own tests we provide a neutral test double (_fixtures/brand.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "_fixtures"))
