jsonwebtoken
============
A Python implementation of `RFC 7519 <https://tools.ietf.org/html/rfc7519>`_. From from `@jpadilla <https://github.com/jpadilla/pyjwt>`_. Original implementation was written by `@progrium <https://github.com/progrium>`_.

Installing
----------

Install with **pip**:

.. code-block:: console

    $ pip install jsonwebtoken


Usage
-----

.. code-block:: pycon

    >>> import jsonwebtoken
    >>> encoded = jsonwebtoken.encode({"some": "payload"}, "secret", algorithm="HS256")
    >>> print(encoded)
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
    >>> jsonwebtken.decode(encoded, "secret", algorithms=["HS256"])
    {'some': 'payload'}

Documentation
-------------

View the full docs online at coming soon