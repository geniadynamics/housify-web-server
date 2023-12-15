import hashlib
from uuid import UUID


def hash_combined_passwd(password: str, user_uuid: UUID) -> bytes:
    """ """
    combined = password + str(user_uuid)

    return hashlib.sha3_512(combined.encode()).digest()
