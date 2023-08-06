import jsonwebtoken

from .utils import utc_timestamp


def test_encode_decode():
    """
    This test exists primarily to ensure that calls to jsonwebtoken.encode and
    jsonwebtoken.decode don't explode. Most functionality is tested by the Pyjsonwebtoken class
    tests. This is primarily a sanity check to make sure we don't break the
    public global functions.
    """
    payload = {"iss": "jeff", "exp": utc_timestamp() + 15, "claim": "insanity"}

    secret = "secret"
    jsonwebtoken_message = jsonwebtoken.encode(payload, secret, algorithm="HS256")
    decoded_payload = jsonwebtoken.decode(jsonwebtoken_message, secret, algorithms=["HS256"])

    assert decoded_payload == payload
