pytest-bdd-html
===============

**Version**: 0.1.9a0

A ``pytest`` plugin to display `BDD <https://en.wikipedia.org/wiki/Behavior-driven_development>`_ info in the ``pytest-html``-generated HTML test report.

Depends on ``pytest-bdd`` and ``pytest-html``.

To use it, just install it. There will be a new 3rd column with label "Description".

Options
-------
Available command line options:

* ``--bdd-html-css=PATH``: specify a path to a custom CSS file for styling of the Description column (``pytest_bdd_html/resources/style.css`` is the default)
  
CSS classes
-----------

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

Structure of cell for non-BDD test without functional comment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  .col-description
    .col-description-no-doc /* an empty div */

