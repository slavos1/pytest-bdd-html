pytest-bdd-html
===============

.. image:: https://img.shields.io/badge/dynamic/xml?url=https://pypi.org/rss/project/pytest-bdd-html/releases.xml&label=pypi&query=//item[1]/title&color=blue
    :target: https://pypi.org/project/pytest-bdd-html/#history
    :alt: PyPI release
.. image:: https://img.shields.io/github/issues/slavos1/pytest-bdd-html
   :target: https://github.com/slavos1/pytest-bdd-html/issues
   :alt: Issues
.. image:: https://img.shields.io/badge/license-MIT-blue
   :target: https://github.com/slavos1/pytest-bdd-html/blob/main/LICENSE
   :alt: License

A ``pytest`` plugin to display `BDD <https://en.wikipedia.org/wiki/Behavior-driven_development>`_ info in the `pytest-html <https://pypi.org/project/pytest-html/>`_-generated HTML test report.

Apart from ``pytest-html``, it plugs into `pytest-bdd <https://pypi.org/project/pytest-bdd/>`_ plugin's hooks.

Usage
----------
To use the plugin, just install it:

.. code:: shell

    # source .venv/bin/activate
    pip install pytest-bdd-html
    pytest -vv ...

If you use `tox <https://pypi.org/project/tox/>`_, list the plugin as a dependency:

.. code:: ini

    ; tox.ini
    [testenv]
    deps = ...
        pytest-bdd-html

    commands = pytest -vv ...

There will be a new *3rd column* with label "Description" in the test report specified by ``--html=...`` command line option of ``pytest-html``.

Command line options
--------------------

Available command line options are as follows.

``--bdd-html-css=PATH``
    Specifies a path to a custom CSS file for styling of the Description column. ``pytest_bdd_html/resources/style.css`` is used by default if ``PATH`` does not exist or is not specified. See `CSS classes`_ for how the column cells are structured.

CSS classes
-----------

For each test case (one row in the ``pytest-html``-generated HTML report), the Description column's cell has one of the following structures, differing for BDD and non-BDD tests (``.XXX`` denotes a HTML element with CSS ``class="XXX"``).

Structure of cell for BDD test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  .col-description
    .col-description-bdd-doc
      /* Feature */
      div
        h3
        .text
           div /* feature name */
           div /* feature description; optional */

      /* Scenario */
      div
        h3
        .text

      /* Steps */
      div
        h3
        .steps
          .step /* one or more steps */
            .step-name
            .step-message

Structure of cell for non-BDD test with functional comment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  .col-description
    .col-description-func-doc

Structure of cell for non-BDD test *without* functional comment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  .col-description
    .col-description-no-doc /* an empty div */

Version update
--------------

::

  bumpver test -p 0.1.13a0 "MAJOR.MINOR.PATCH[PYTAGNUM]"
  bumpver update -n -d -p
  bumpver update -n -p

