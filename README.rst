Okta Authentication
==========================

This is a plugin for `pretix`_. 

Supports pretix backend auth using Okta

Production setup
----------------

As this is not on PyPI for now, install from git::

    pip install git+https://github.com/pretix/pretix-auth-okta.git@master#egg=pretix-auth-okta

Configuration
-------------

First, you nmeed to create a web application in Okta. The redirect URL is ``https://<pretixserver>/_okta/return``.

Then, you need to tweak your ``pretix.cfg`` file like this::

    [pretix]  ; add to your existing section
    auth_backends=pretix_auth_okta.auth.OktaAuthBackend,pretix.base.auth.NativeAuthBackend

    [pretix_auth_okta]
    label=My Company SSO
    client_id=123456
    client_secret=5675345
    url=https://dev-123456.okta.com/oauth2

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-auth-okta``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------


Copyright 2020 pretix Team

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
