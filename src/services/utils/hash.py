import hashlib
from uuid import UUID


def hash_combined_passwd(password: str, user_uuid: UUID) -> str:
    """ """
    return hashlib.sha3_512((password + user_uuid.hex).encode()).hexdigest()
