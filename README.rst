python-keyutils
===============

python-keyutils is a set of python bindings for keyutils (available from
http://people.redhat.com/~dhowells/keyutils), a key management suite that
leverages the infrastructure provided by the Linux kernel for safely storing
and retrieving sensitive infromation in your programs.

Usage
~~~~~

The C extension module follows closely the C API (see ``add_key(2)``,
``request_key(2)``, ``keyctl_read_alloc(2)``).

Exceptions also follow the C API. The only notable difference is for
``request_key``: when the key is not present, ``None`` is returned, instead of
raising an exception (which is usually a more expensive operation).

Note that the function parameters are passed as bytes not strings! On python 3
this usually requires an explicit ``param.encode()`` call.

For example:

.. code-block:: python

    import keyutils

    # NOTE: only pass `bytes` to the keyutils API:
    name = b'foo'
    value = b'bar'
    ring = keyutils.KEY_SPEC_PROCESS_KEYRING

    key_id = keyutils.add_key(name, value, ring)

    assert keyutils.request_key(name, ring) == key_id
    assert keyutils.read_key(key_id) == value

    # set timeout to 5 seconds, wait and then... it's gone:
    keyutils.set_timeout(key_id, 5)
    from time import sleep
    sleep(6)
    assert keyutils.request_key(name, ring) == None


Further examples can be found in the ``tests`` subfolder.
