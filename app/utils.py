from hashids import Hashids
from django.conf import settings

hashids = Hashids(salt=settings.HASH_KEY, min_length=8)


def encode_id(numeric_id):
    return hashids.encode(numeric_id)

def decode_id(hashed_id):
    decoded = hashids.decode(hashed_id)
    if decoded:
        return decoded[0]
    return None
