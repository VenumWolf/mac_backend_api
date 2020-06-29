==============================
Mind Audio Central Backend API
==============================

The Basics
----------

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy mac_backend_api

Running Tests
^^^^^^^^^^^^^

To run the tests:

::

  $ pytest

Generating Coverage Reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ pytest --cov-report html --cov=mac_backend_api

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

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
