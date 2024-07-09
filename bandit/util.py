import hashlib
from collections import OrderedDict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bandit.state import State


def generate_hash(object_state) -> str:
    """
    Generates a hash for the object with md5 encryption.

    The hash is generated from the object state.

    Parameters
    ----------
    object_state (Object):
        The object to generate a hash for

    Returns
    -------
    str:
        The hash of the object
    """

    object_state_str = str(object_state)
    state_bytes = object_state_str.encode("utf-8")

    hash_md5 = hashlib.md5()
    hash_md5.update(state_bytes)
    return hash_md5.hexdigest()


class LimitedDict(OrderedDict):
    """
    A dictionary with a limit on the number of items it can store.

    When the limit is reached, the oldest item is removed.

    Parameters
    ----------
    limit : int
        The maximum number of items to store.
    """

    def __init__(self, limit: int, *args, **kwargs) -> None:
        self.limit = limit
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets the value of the key.
        """
        if key in self:
            del self[key]
        elif len(self) >= self.limit:
            self.popitem(last=False)
        super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        """
        Returns whether the key is in the dictionary.
        """
        return key in self.keys()
