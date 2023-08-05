from __future__ import annotations


class EmptyKeyError(ValueError):
    pass


class KeyAlreadySetError(ValueError):
    pass


class KeyDoesNotExistError(KeyError):
    pass


EMPTY_KEY_ERROR = EmptyKeyError("Key cannot be empty")
KEY_ALREADY_SET_ERROR = KeyAlreadySetError("Key is already set")
