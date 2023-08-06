import json
import time
from calendar import timegm
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from jsonwebtoken.api_jsonwebtoken import Pyjsonwebtoken
from jsonwebtoken.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    MissingRequiredClaimError,
)
from jsonwebtoken.utils import base64url_decode
from jsonwebtoken.warnings import RemovedInPyjsonwebtoken3Warning

from .utils import crypto_required, key_path, utc_timestamp


@pytest.fixture
def jsonwebtoken():
    return Pyjsonwebtoken()


@pytest.fixture
def payload():
    """Creates a sample jsonwebtoken claimset for use as a payload during tests"""
    return {"iss": "jeff", "exp": utc_timestamp() + 15, "claim": "insanity"}


class Testjsonwebtoken:
    def test_decodes_valid_jsonwebtoken(self, jsonwebtoken):
        example_payload = {"hello": "world"}
        example_secret = "secret"
        example_jsonwebtoken = (
            b"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9"
            b".eyJoZWxsbyI6ICJ3b3JsZCJ9"
            b".tvagLDLoaiJKxOKqpBXSEGy7SYSifZhjntgm9ctpyj8"
        )
        decoded_payload = jsonwebtoken.decode(example_jsonwebtoken, example_secret, algorithms=["HS256"])

        assert decoded_payload == example_payload

    def test_decodes_complete_valid_jsonwebtoken(self, jsonwebtoken):
        example_payload = {"hello": "world"}
        example_secret = "secret"
        example_jsonwebtoken = (
            b"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9"
            b".eyJoZWxsbyI6ICJ3b3JsZCJ9"
            b".tvagLDLoaiJKxOKqpBXSEGy7SYSifZhjntgm9ctpyj8"
        )
        decoded = jsonwebtoken.decode_complete(example_jsonwebtoken, example_secret, algorithms=["HS256"])

        assert decoded == {
            "header": {"alg": "HS256", "typ": "jsonwebtoken"},
            "payload": example_payload,
            "signature": (
                b'\xb6\xf6\xa0,2\xe8j"J\xc4\xe2\xaa\xa4\x15\xd2'
                b"\x10l\xbbI\x84\xa2}\x98c\x9e\xd8&\xf5\xcbi\xca?"
            ),
        }

    def test_load_verify_valid_jsonwebtoken(self, jsonwebtoken):
        example_payload = {"hello": "world"}
        example_secret = "secret"
        example_jsonwebtoken = (
            b"eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9"
            b".eyJoZWxsbyI6ICJ3b3JsZCJ9"
            b".tvagLDLoaiJKxOKqpBXSEGy7SYSifZhjntgm9ctpyj8"
        )

        decoded_payload = jsonwebtoken.decode(
            example_jsonwebtoken, key=example_secret, algorithms=["HS256"]
        )

        assert decoded_payload == example_payload

    def test_decode_invalid_payload_string(self, jsonwebtoken):
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.aGVsb"
            "G8gd29ybGQ.SIr03zM64awWRdPrAM_61QWsZchAtgDV"
            "3pphfHPPWkI"
        )
        example_secret = "secret"

        with pytest.raises(DecodeError) as exc:
            jsonwebtoken.decode(example_jsonwebtoken, example_secret, algorithms=["HS256"])

        assert "Invalid payload string" in str(exc.value)

    def test_decode_with_non_mapping_payload_throws_exception(self, jsonwebtoken):
        secret = "secret"
        example_jsonwebtoken = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "MQ."  # == 1
            "AbcSR3DWum91KOgfKxUHm78rLs_DrrZ1CrDgpUFFzls"
        )

        with pytest.raises(DecodeError) as context:
            jsonwebtoken.decode(example_jsonwebtoken, secret, algorithms=["HS256"])

        exception = context.value
        assert str(exception) == "Invalid payload string: must be a json object"

    def test_decode_with_invalid_audience_param_throws_exception(self, jsonwebtoken):
        secret = "secret"
        example_jsonwebtoken = (
            "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9"
            ".eyJoZWxsbyI6ICJ3b3JsZCJ9"
            ".tvagLDLoaiJKxOKqpBXSEGy7SYSifZhjntgm9ctpyj8"
        )

        with pytest.raises(TypeError) as context:
            jsonwebtoken.decode(example_jsonwebtoken, secret, audience=1, algorithms=["HS256"])

        exception = context.value
        assert str(exception) == "audience must be a string, iterable or None"

    def test_decode_with_nonlist_aud_claim_throws_exception(self, jsonwebtoken):
        secret = "secret"
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJoZWxsbyI6IndvcmxkIiwiYXVkIjoxfQ"  # aud = 1
            ".Rof08LBSwbm8Z_bhA2N3DFY-utZR1Gi9rbIS5Zthnnc"
        )

        with pytest.raises(InvalidAudienceError) as context:
            jsonwebtoken.decode(
                example_jsonwebtoken,
                secret,
                audience="my_audience",
                algorithms=["HS256"],
            )

        exception = context.value
        assert str(exception) == "Invalid claim format in token"

    def test_decode_with_invalid_aud_list_member_throws_exception(self, jsonwebtoken):
        secret = "secret"
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJoZWxsbyI6IndvcmxkIiwiYXVkIjpbMV19"
            ".iQgKpJ8shetwNMIosNXWBPFB057c2BHs-8t1d2CCM2A"
        )

        with pytest.raises(InvalidAudienceError) as context:
            jsonwebtoken.decode(
                example_jsonwebtoken,
                secret,
                audience="my_audience",
                algorithms=["HS256"],
            )

        exception = context.value
        assert str(exception) == "Invalid claim format in token"

    def test_encode_bad_type(self, jsonwebtoken):

        types = ["string", tuple(), list(), 42, set()]

        for t in types:
            pytest.raises(
                TypeError,
                lambda: jsonwebtoken.encode(t, "secret", algorithms=["HS256"]),
            )

    def test_encode_with_typ(self, jsonwebtoken):
        payload = {
            "iss": "https://scim.example.com",
            "iat": 1458496404,
            "jti": "4d3559ec67504aaba65d40b0363faad8",
            "aud": [
                "https://scim.example.com/Feeds/98d52461fa5bbc879593b7754",
                "https://scim.example.com/Feeds/5d7604516b1d08641d7676ee7",
            ],
            "events": {
                "urn:ietf:params:scim:event:create": {
                    "ref": "https://scim.example.com/Users/44f6142df96bd6ab61e7521d9",
                    "attributes": ["id", "name", "userName", "password", "emails"],
                }
            },
        }
        token = jsonwebtoken.encode(
            payload, "secret", algorithm="HS256", headers={"typ": "secevent+jsonwebtoken"}
        )
        header = token[0 : token.index(".")].encode()
        header = base64url_decode(header)
        header_obj = json.loads(header)

        assert "typ" in header_obj
        assert header_obj["typ"] == "secevent+jsonwebtoken"

    def test_decode_raises_exception_if_exp_is_not_int(self, jsonwebtoken):
        # >>> jsonwebtoken.encode({'exp': 'not-an-int'}, 'secret')
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJleHAiOiJub3QtYW4taW50In0."
            "P65iYgoHtBqB07PMtBSuKNUEIPPPfmjfJG217cEE66s"
        )

        with pytest.raises(DecodeError) as exc:
            jsonwebtoken.decode(example_jsonwebtoken, "secret", algorithms=["HS256"])

        assert "exp" in str(exc.value)

    def test_decode_raises_exception_if_iat_is_not_int(self, jsonwebtoken):
        # >>> jsonwebtoken.encode({'iat': 'not-an-int'}, 'secret')
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJpYXQiOiJub3QtYW4taW50In0."
            "H1GmcQgSySa5LOKYbzGm--b1OmRbHFkyk8pq811FzZM"
        )

        with pytest.raises(InvalidIssuedAtError):
            jsonwebtoken.decode(example_jsonwebtoken, "secret", algorithms=["HS256"])

    def test_decode_raises_exception_if_iat_is_greater_than_now(self, jsonwebtoken, payload):
        payload["iat"] = utc_timestamp() + 10
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.raises(ImmatureSignatureError):
            jsonwebtoken.decode(jsonwebtoken_message, secret, algorithms=["HS256"])

    def test_decode_raises_exception_if_nbf_is_not_int(self, jsonwebtoken):
        # >>> jsonwebtoken.encode({'nbf': 'not-an-int'}, 'secret')
        example_jsonwebtoken = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJuYmYiOiJub3QtYW4taW50In0."
            "c25hldC8G2ZamC8uKpax9sYMTgdZo3cxrmzFHaAAluw"
        )

        with pytest.raises(DecodeError):
            jsonwebtoken.decode(example_jsonwebtoken, "secret", algorithms=["HS256"])

    def test_decode_raises_exception_if_aud_is_none(self, jsonwebtoken):
        # >>> jsonwebtoken.encode({'aud': None}, 'secret')
        example_jsonwebtoken = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJhdWQiOm51bGx9."
            "-Peqc-pTugGvrc5C8Bnl0-X1V_5fv-aVb_7y7nGBVvQ"
        )
        decoded = jsonwebtoken.decode(example_jsonwebtoken, "secret", algorithms=["HS256"])
        assert decoded["aud"] is None

    def test_encode_datetime(self, jsonwebtoken):
        secret = "secret"
        current_datetime = datetime.now(tz=timezone.utc)
        payload = {
            "exp": current_datetime,
            "iat": current_datetime,
            "nbf": current_datetime,
        }
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)
        decoded_payload = jsonwebtoken.decode(
            jsonwebtoken_message, secret, leeway=1, algorithms=["HS256"]
        )

        assert decoded_payload["exp"] == timegm(current_datetime.utctimetuple())
        assert decoded_payload["iat"] == timegm(current_datetime.utctimetuple())
        assert decoded_payload["nbf"] == timegm(current_datetime.utctimetuple())
        # payload is not mutated.
        assert payload == {
            "exp": current_datetime,
            "iat": current_datetime,
            "nbf": current_datetime,
        }

    # 'Control' Elliptic Curve jsonwebtoken created by another library.
    # Used to test for regressions that could affect both
    # encoding / decoding operations equally (causing tests
    # to still pass).
    @crypto_required
    def test_decodes_valid_es256_jsonwebtoken(self, jsonwebtoken):
        example_payload = {"hello": "world"}
        with open(key_path("testkey_ec.pub")) as fp:
            example_pubkey = fp.read()
        example_jsonwebtoken = (
            b"eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9."
            b"eyJoZWxsbyI6IndvcmxkIn0.TORyNQab_MoXM7DvNKaTwbrJr4UY"
            b"d2SsX8hhlnWelQFmPFSf_JzC2EbLnar92t-bXsDovzxp25ExazrVHkfPkQ"
        )

        decoded_payload = jsonwebtoken.decode(example_jsonwebtoken, example_pubkey, algorithms=["ES256"])
        assert decoded_payload == example_payload

    # 'Control' RSA jsonwebtoken created by another library.
    # Used to test for regressions that could affect both
    # encoding / decoding operations equally (causing tests
    # to still pass).
    @crypto_required
    def test_decodes_valid_rs384_jsonwebtoken(self, jsonwebtoken):
        example_payload = {"hello": "world"}
        with open(key_path("testkey_rsa.pub")) as fp:
            example_pubkey = fp.read()
        example_jsonwebtoken = (
            b"eyJhbGciOiJSUzM4NCIsInR5cCI6IkpXVCJ9"
            b".eyJoZWxsbyI6IndvcmxkIn0"
            b".yNQ3nI9vEDs7lEh-Cp81McPuiQ4ZRv6FL4evTYYAh1X"
            b"lRTTR3Cz8pPA9Stgso8Ra9xGB4X3rlra1c8Jz10nTUju"
            b"O06OMm7oXdrnxp1KIiAJDerWHkQ7l3dlizIk1bmMA457"
            b"W2fNzNfHViuED5ISM081dgf_a71qBwJ_yShMMrSOfxDx"
            b"mX9c4DjRogRJG8SM5PvpLqI_Cm9iQPGMvmYK7gzcq2cJ"
            b"urHRJDJHTqIdpLWXkY7zVikeen6FhuGyn060Dz9gYq9t"
            b"uwmrtSWCBUjiN8sqJ00CDgycxKqHfUndZbEAOjcCAhBr"
            b"qWW3mSVivUfubsYbwUdUG3fSRPjaUPcpe8A"
        )
        decoded_payload = jsonwebtoken.decode(example_jsonwebtoken, example_pubkey, algorithms=["RS384"])

        assert decoded_payload == example_payload

    def test_decode_with_expiration(self, jsonwebtoken, payload):
        payload["exp"] = utc_timestamp() - 1
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.raises(ExpiredSignatureError):
            jsonwebtoken.decode(jsonwebtoken_message, secret, algorithms=["HS256"])

    def test_decode_with_notbefore(self, jsonwebtoken, payload):
        payload["nbf"] = utc_timestamp() + 10
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.raises(ImmatureSignatureError):
            jsonwebtoken.decode(jsonwebtoken_message, secret, algorithms=["HS256"])

    def test_decode_skip_expiration_verification(self, jsonwebtoken, payload):
        payload["exp"] = time.time() - 1
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        jsonwebtoken.decode(
            jsonwebtoken_message,
            secret,
            algorithms=["HS256"],
            options={"verify_exp": False},
        )

    def test_decode_skip_notbefore_verification(self, jsonwebtoken, payload):
        payload["nbf"] = time.time() + 10
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        jsonwebtoken.decode(
            jsonwebtoken_message,
            secret,
            algorithms=["HS256"],
            options={"verify_nbf": False},
        )

    def test_decode_with_expiration_with_leeway(self, jsonwebtoken, payload):
        payload["exp"] = utc_timestamp() - 2
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        # With 3 seconds leeway, should be ok
        for leeway in (3, timedelta(seconds=3)):
            decoded = jsonwebtoken.decode(
                jsonwebtoken_message, secret, leeway=leeway, algorithms=["HS256"]
            )
            assert decoded == payload

        # With 1 seconds, should fail
        for leeway in (1, timedelta(seconds=1)):
            with pytest.raises(ExpiredSignatureError):
                jsonwebtoken.decode(jsonwebtoken_message, secret, leeway=leeway, algorithms=["HS256"])

    def test_decode_with_notbefore_with_leeway(self, jsonwebtoken, payload):
        payload["nbf"] = utc_timestamp() + 10
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        # With 13 seconds leeway, should be ok
        jsonwebtoken.decode(jsonwebtoken_message, secret, leeway=13, algorithms=["HS256"])

        with pytest.raises(ImmatureSignatureError):
            jsonwebtoken.decode(jsonwebtoken_message, secret, leeway=1, algorithms=["HS256"])

    def test_check_audience_when_valid(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:me"}
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(token, "secret", audience="urn:me", algorithms=["HS256"])

    def test_check_audience_list_when_valid(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:me"}
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(
            token,
            "secret",
            audience=["urn:you", "urn:me"],
            algorithms=["HS256"],
        )

    def test_check_audience_none_specified(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:me"}
        token = jsonwebtoken.encode(payload, "secret")
        with pytest.raises(InvalidAudienceError):
            jsonwebtoken.decode(token, "secret", algorithms=["HS256"])

    def test_raise_exception_invalid_audience_list(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:me"}
        token = jsonwebtoken.encode(payload, "secret")
        with pytest.raises(InvalidAudienceError):
            jsonwebtoken.decode(
                token,
                "secret",
                audience=["urn:you", "urn:him"],
                algorithms=["HS256"],
            )

    def test_check_audience_in_array_when_valid(self, jsonwebtoken):
        payload = {"some": "payload", "aud": ["urn:me", "urn:someone-else"]}
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(token, "secret", audience="urn:me", algorithms=["HS256"])

    def test_raise_exception_invalid_audience(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:someone-else"}

        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(InvalidAudienceError):
            jsonwebtoken.decode(token, "secret", audience="urn-me", algorithms=["HS256"])

    def test_raise_exception_audience_as_bytes(self, jsonwebtoken):
        payload = {"some": "payload", "aud": ["urn:me", "urn:someone-else"]}
        token = jsonwebtoken.encode(payload, "secret")
        with pytest.raises(InvalidAudienceError):
            jsonwebtoken.decode(
                token, "secret", audience="urn:me".encode(), algorithms=["HS256"]
            )

    def test_raise_exception_invalid_audience_in_array(self, jsonwebtoken):
        payload = {
            "some": "payload",
            "aud": ["urn:someone", "urn:someone-else"],
        }

        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(InvalidAudienceError):
            jsonwebtoken.decode(token, "secret", audience="urn:me", algorithms=["HS256"])

    def test_raise_exception_token_without_issuer(self, jsonwebtoken):
        issuer = "urn:wrong"

        payload = {"some": "payload"}

        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(token, "secret", issuer=issuer, algorithms=["HS256"])

        assert exc.value.claim == "iss"

    def test_raise_exception_token_without_audience(self, jsonwebtoken):
        payload = {"some": "payload"}
        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(token, "secret", audience="urn:me", algorithms=["HS256"])

        assert exc.value.claim == "aud"

    def test_raise_exception_token_with_aud_none_and_without_audience(self, jsonwebtoken):
        payload = {"some": "payload", "aud": None}
        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(token, "secret", audience="urn:me", algorithms=["HS256"])

        assert exc.value.claim == "aud"

    def test_check_issuer_when_valid(self, jsonwebtoken):
        issuer = "urn:foo"
        payload = {"some": "payload", "iss": "urn:foo"}
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(token, "secret", issuer=issuer, algorithms=["HS256"])

    def test_raise_exception_invalid_issuer(self, jsonwebtoken):
        issuer = "urn:wrong"

        payload = {"some": "payload", "iss": "urn:foo"}

        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(InvalidIssuerError):
            jsonwebtoken.decode(token, "secret", issuer=issuer, algorithms=["HS256"])

    def test_skip_check_audience(self, jsonwebtoken):
        payload = {"some": "payload", "aud": "urn:me"}
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(
            token,
            "secret",
            options={"verify_aud": False},
            algorithms=["HS256"],
        )

    def test_skip_check_exp(self, jsonwebtoken):
        payload = {
            "some": "payload",
            "exp": datetime.now(tz=timezone.utc) - timedelta(days=1),
        }
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(
            token,
            "secret",
            options={"verify_exp": False},
            algorithms=["HS256"],
        )

    def test_decode_should_raise_error_if_exp_required_but_not_present(self, jsonwebtoken):
        payload = {
            "some": "payload",
            # exp not present
        }
        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(
                token,
                "secret",
                options={"require": ["exp"]},
                algorithms=["HS256"],
            )

        assert exc.value.claim == "exp"

    def test_decode_should_raise_error_if_iat_required_but_not_present(self, jsonwebtoken):
        payload = {
            "some": "payload",
            # iat not present
        }
        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(
                token,
                "secret",
                options={"require": ["iat"]},
                algorithms=["HS256"],
            )

        assert exc.value.claim == "iat"

    def test_decode_should_raise_error_if_nbf_required_but_not_present(self, jsonwebtoken):
        payload = {
            "some": "payload",
            # nbf not present
        }
        token = jsonwebtoken.encode(payload, "secret")

        with pytest.raises(MissingRequiredClaimError) as exc:
            jsonwebtoken.decode(
                token,
                "secret",
                options={"require": ["nbf"]},
                algorithms=["HS256"],
            )

        assert exc.value.claim == "nbf"

    def test_skip_check_signature(self, jsonwebtoken):
        token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzb21lIjoicGF5bG9hZCJ9"
            ".4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZA"
        )
        jsonwebtoken.decode(
            token,
            "secret",
            options={"verify_signature": False},
            algorithms=["HS256"],
        )

    def test_skip_check_iat(self, jsonwebtoken):
        payload = {
            "some": "payload",
            "iat": datetime.now(tz=timezone.utc) + timedelta(days=1),
        }
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(
            token,
            "secret",
            options={"verify_iat": False},
            algorithms=["HS256"],
        )

    def test_skip_check_nbf(self, jsonwebtoken):
        payload = {
            "some": "payload",
            "nbf": datetime.now(tz=timezone.utc) + timedelta(days=1),
        }
        token = jsonwebtoken.encode(payload, "secret")
        jsonwebtoken.decode(
            token,
            "secret",
            options={"verify_nbf": False},
            algorithms=["HS256"],
        )

    def test_custom_json_encoder(self, jsonwebtoken):
        class CustomJSONEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, Decimal):
                    return "it worked"
                return super().default(o)

        data = {"some_decimal": Decimal("2.2")}

        with pytest.raises(TypeError):
            jsonwebtoken.encode(data, "secret", algorithms=["HS256"])

        token = jsonwebtoken.encode(data, "secret", json_encoder=CustomJSONEncoder)
        payload = jsonwebtoken.decode(token, "secret", algorithms=["HS256"])

        assert payload == {"some_decimal": "it worked"}

    def test_decode_with_verify_exp_option(self, jsonwebtoken, payload):
        payload["exp"] = utc_timestamp() - 1
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        jsonwebtoken.decode(
            jsonwebtoken_message,
            secret,
            algorithms=["HS256"],
            options={"verify_exp": False},
        )

        with pytest.raises(ExpiredSignatureError):
            jsonwebtoken.decode(
                jsonwebtoken_message,
                secret,
                algorithms=["HS256"],
                options={"verify_exp": True},
            )

    def test_decode_with_verify_exp_option_and_signature_off(self, jsonwebtoken, payload):
        payload["exp"] = utc_timestamp() - 1
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        jsonwebtoken.decode(
            jsonwebtoken_message,
            options={"verify_signature": False},
        )

        with pytest.raises(ExpiredSignatureError):
            jsonwebtoken.decode(
                jsonwebtoken_message,
                options={"verify_signature": False, "verify_exp": True},
            )

    def test_decode_with_optional_algorithms(self, jsonwebtoken, payload):
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.raises(DecodeError) as exc:
            jsonwebtoken.decode(jsonwebtoken_message, secret)

        assert (
            'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            in str(exc.value)
        )

    def test_decode_no_algorithms_verify_signature_false(self, jsonwebtoken, payload):
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        jsonwebtoken.decode(jsonwebtoken_message, secret, options={"verify_signature": False})

    def test_decode_legacy_verify_warning(self, jsonwebtoken, payload):
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.deprecated_call():
            # The implicit default for options.verify_signature is True,
            # but the user sets verify to False.
            jsonwebtoken.decode(jsonwebtoken_message, secret, verify=False, algorithms=["HS256"])

        with pytest.deprecated_call():
            # The user explicitly sets verify=True,
            # but contradicts it in verify_signature.
            jsonwebtoken.decode(
                jsonwebtoken_message, secret, verify=True, options={"verify_signature": False}
            )

    def test_decode_no_options_mutation(self, jsonwebtoken, payload):
        options = {"verify_signature": True}
        orig_options = options.copy()
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)
        jsonwebtoken.decode(jsonwebtoken_message, secret, options=options, algorithms=["HS256"])
        assert options == orig_options

    def test_decode_warns_on_unsupported_kwarg(self, jsonwebtoken, payload):
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.warns(RemovedInPyjsonwebtoken3Warning) as record:
            jsonwebtoken.decode(jsonwebtoken_message, secret, algorithms=["HS256"], foo="bar")
        assert len(record) == 1
        assert "foo" in str(record[0].message)

    def test_decode_complete_warns_on_unsupported_kwarg(self, jsonwebtoken, payload):
        secret = "secret"
        jsonwebtoken_message = jsonwebtoken.encode(payload, secret)

        with pytest.warns(RemovedInPyjsonwebtoken3Warning) as record:
            jsonwebtoken.decode_complete(jsonwebtoken_message, secret, algorithms=["HS256"], foo="bar")
        assert len(record) == 1
        assert "foo" in str(record[0].message)
