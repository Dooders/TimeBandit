import hashlib


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
