from .taglist import TagList, keyTupleLoads, tupleStrParse
from .csvlist import SingleColumnCSV
from .gitsync import GitSyncControl
from .config import DefaultConfig


def syncControl(
    *args,
    **kwargs,
) -> GitSyncControl:
    """Create a :class:`GitSyncControl` object.

    Returns:
        GitSyncControl: A :class:`GitSyncControl` object.
    """
    return GitSyncControl(*args, **kwargs)
