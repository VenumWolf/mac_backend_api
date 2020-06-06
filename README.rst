==============================
Mind Audio Central Backend API
==============================

Monolithic backend system for Mind Audio Central.

The Basics
----------

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy mac_backend_api

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application.  While in a
development environment, MailHog is used to provide a simple SMTP server and a web interface.

#. `Download the latest MailHog release`_ for your OS.

#. Rename the build to ``MailHog``.

#. Copy the file to the project root.

#. Make it executable: ::

    $ chmod +x MailHog

#. Spin up another terminal window and start it there: ::

    ./MailHog

#. Check out `<http://127.0.0.1:8025/>`_ to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog/releases
