
.. _readme:

RKVST Simplehash in python
============================

Prescribed python code that defines the hashing algorithm for DLT Anchoring.

Support
=========

This package currently is tested against Python versions 3.7,3.8,3.9, 3.10 and 3.11.

The current default version is 3.7 - this means that this package will not
use any features specific to versions 3.8 and later.

After End of Life of a particular Python version, support is offered on a best effort
basis. We may ask you to update your Python version to help solve the problem,
if it cannot be reasonably resolved in your current version.

Installation
==============

Use standard python pip utility:

.. code:: bash

    python3 -m pip install rkvst-simplehash

If your version of python3 is too old an error of this type or similar will be emitted:

.. note::

    ERROR: Could not find a version that satisfies the requirement rkvst-simplehash (from versions: none)
    ERROR: No matching distribution found for rkvst-simplehash

Which Version
===============

To Determine which version of the simple hash script to use, i.e. simplehashv1 or simplehashv2,
look at the response from the `v1alpha2/blockchain` list api and correlate the version with the `hash_schema_version`
in the `simple_hash_details` section.

Alternatively look for the SimpleHashInfo section in the rkvst app, found on the transaction page
of a simple hash event, and correlate the version with `schema_version`.

Examples
==========

You can then use the code to recreate the simple hash of a list of SIMPLE_HASH events from RKVST.

Importing in own code
------------------------

Permissioned Assets V1
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v1 import (
        anchor_events,
        SimpleHashError,
    )

    with open("credentials/token", mode="r", encoding="utf-8") as tokenfile:
        auth_token = tokenfile.read().strip()

    # SimpleHashClientAuthError is raised if the auth token is invalid or expired.
    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown
    api_query = (
        "https://app.rkvst.io"
        "/archivist/v2/assets/-/events"
        "?proof_mechanism=SIMPLE_HASH"
        "&timestamp_accepted_since=2022-10-07T07:01:34Z"
        "&timestamp_accepted_before=2022-10-16T13:14:56Z"
        "&order_by=SIMPLEHASHV1"
    )
    try:
        simplehash = anchor_events(api_query, auth=auth_token)
    except SimpleHashError as ex:
        print("Error", ex)

    else:
        print("simplehash=", simplehash)

Permissioned Assets V2
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v2 import (
        anchor_events,
        SimpleHashError,
    )

    with open("credentials/token", mode="r", encoding="utf-8") as tokenfile:
        auth_token = tokenfile.read().strip()

    # SimpleHashClientAuthError is raised if the auth token is invalid or expired.
    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown
    api_query = (
        "https://app.rkvst.io"
        "/archivist/v2/assets/-/events"
        "?proof_mechanism=SIMPLE_HASH"
        "&timestamp_accepted_since=2022-10-07T07:01:34Z"
        "&timestamp_accepted_before=2022-10-16T13:14:56Z"
        "&order_by=SIMPLEHASHV1"
    )
    try:
        simplehash = anchor_events(api_query, auth=auth_token)
    except SimpleHashError as ex:
        print("Error", ex)

    else:
        print("simplehash=", simplehash)

Public Assets V1
~~~~~~~~~~~~~~~~~

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v1 import (
        anchor_events,
        SimpleHashError,
    )

    # SimpleHashClientAuthError is raised if the auth token is invalid or expired.
    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown
    api_query = (
        "https://app.rkvst.io"
        "/archivist/v2/publicassets/-/events"
        "?proof_mechanism=SIMPLE_HASH"
        "&timestamp_accepted_since=2022-10-07T07:01:34Z"
        "&timestamp_accepted_before=2022-10-16T13:14:56Z"
        "&order_by=SIMPLEHASHV1"
    )
    try:
        simplehash = anchor_events(api_query)
    except SimpleHashError as ex:
        print("Error", ex)

    else:
        print("simplehash=", simplehash)

Public Assets V2
~~~~~~~~~~~~~~~~~

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v2 import (
        anchor_events,
        SimpleHashError,
    )

    # SimpleHashClientAuthError is raised if the auth token is invalid or expired.
    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown
    api_query = (
        "https://app.rkvst.io"
        "/archivist/v2/publicassets/-/events"
        "?proof_mechanism=SIMPLE_HASH"
        "&timestamp_accepted_since=2022-10-07T07:01:34Z"
        "&timestamp_accepted_before=2022-10-16T13:14:56Z"
        "&order_by=SIMPLEHASHV1"
    )
    try:
        simplehash = anchor_events(api_query)
    except SimpleHashError as ex:
        print("Error", ex)

    else:
        print("simplehash=", simplehash)


Command Line
----------------

This functionality is also available on the cmdline.

Using a virtual env and published wheel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This can be executed anywhere using a virtualenv and published wheel.
Credentials are stored in files in credentials directory.

Using an auth token directly and for permissioned assets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/assets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    rkvst_simplehashv1 \
        --auth-token-file "credentials/token" \
        "${api_query}"
    
    deactivate
    rm -rf simplehash-venv

Or for schema version 2:

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/assets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    rkvst_simplehashv2 \
        --auth-token-file "credentials/token" \
        "${api_query}"
    
    deactivate
    rm -rf simplehash-venv

Using a client id and secret and for permissioned assets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/assets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    CLIENT_ID=$(cat credentials/client_id)
    rkvst_simplehashv1 \
        --client-id "${CLIENT_ID}" \
        --client-secret-file "credentials/client_secret" \
        "${api_query}"
    
    deactivate
    rm -rf simplehash-venv

Or for schema version 2:

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/assets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    CLIENT_ID=$(cat credentials/client_id)
    rkvst_simplehashv2 \
        --client-id "${CLIENT_ID}" \
        --client-secret-file "credentials/client_secret" \
        "${api_query}"
    
    deactivate
    rm -rf simplehash-venv

Querying the public assets (does not require authentication)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    start_time = "2022-11-16T00:00:00Z"
    end_time = "2022-11-17T00:00:00Z"
    rkvst_url = "https://app.rkvst.io"
    endpoint = "archivist/v2/publicassets/-/events"
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/publicassets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    rkvst_simplehashv1 "${api_query}"
    
    deactivate
    rm -rf simplehash-venv

Or for schema version 2:

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    start_time = "2022-11-16T00:00:00Z"
    end_time = "2022-11-17T00:00:00Z"
    rkvst_url = "https://app.rkvst.io"
    endpoint = "archivist/v2/publicassets/-/events"
    
    api_query="https://app.rkvst.io"
    api_query+="/archivist/v2/publicassets/-/events"
    api_query+="?proof_mechanism=SIMPLE_HASH"
    api_query+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
    api_query+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
    api_query+="&order_by=SIMPLEHASHV1"

    rkvst_simplehashv2 "${api_query}"
    
    deactivate
    rm -rf simplehash-venv