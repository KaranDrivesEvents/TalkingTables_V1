"""Tools package for TalkingTables ReAct agent."""

from .read_current_dbml import read_current_dbml
from .read_updated_dbml import read_updated_dbml
from .call_dbml_parser import call_dbml_parser
from typing import List


def get_dbml_tools() -> List:
    """Get the list of DBML tools for the ReAct agent."""
    return [
        read_current_dbml,
        read_updated_dbml,
        call_dbml_parser
    ]


__all__ = ["get_dbml_tools", "read_current_dbml", "read_updated_dbml", "call_dbml_parser"] 