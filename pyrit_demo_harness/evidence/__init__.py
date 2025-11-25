"""
Evidence builder module for EU AI Act Annex III-4 compliance.

This module provides functionality to build schema-compliant evidence records
from PYRIT harness execution results.
"""

from .builder import build_evidence_record

__all__ = ["build_evidence_record"]
