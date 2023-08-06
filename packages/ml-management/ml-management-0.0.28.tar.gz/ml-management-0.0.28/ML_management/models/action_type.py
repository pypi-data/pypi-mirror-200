"""List of action types for vertex of version graph."""
from enum import Enum


class ActionType(str, Enum):
    """List of action types for vertex of version graph."""

    UPLOAD = "upload"
    TRAIN = "train"
    FINETUNE = "finetune"
