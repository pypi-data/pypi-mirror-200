============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.com/ethz_hvl/hvl_ccb/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitLab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitLab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

HVL Common Code Base could always use more documentation, whether as part of the
official HVL Common Code Base docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.com/ethz_hvl/hvl_ccb/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `hvl_ccb` for local development.

1. Clone `hvl_ccb` repo from GitLab::

    $ git clone git@gitlab.com:ethz_hvl/hvl_ccb.git

2. Go into the cloned folder. Then install your virtual environment and activate it::

    $ cd hvl_ccb
    $ python -m venv .venv
    $ . .venv/Scripts/activate  # <-- for Windows
    $ . .venv_22/bin/activate   # <-- for Linux

3. Install the HVL-CommonCodeBase with its dependencies as well as the dependencies for development::

    $ pip install -e .[all]
    $ pip install -r requirements_dev.txt

4. Furthermore, it is recommended to install the git hook script shipped within the repository::

    $ pre-commit install

5. After creating an Issue and Merge Reqeust on GitLab, you can switch to you created development branch::

    $ git switch name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8, mypy, black, isort and the
   tests, including testing other Python versions with tox::

    $ isort .
    $ black --preview hvl_ccb/ tests/ examples/
    $ flake8 hvl_ccb tests
    $ mypy --show-error-codes hvl_ccb
    $ python setup.py test or py.test
    $ tox

   You can also use the provided make-like shell script to run flake8 and tests::

   $ ./make.sh black
   $ ./make.sh isort
   $ ./make.sh style
   $ ./make.sh type
   $ ./make.sh test

7. As we want to maintain a high quality of coding style we use `black` and `isort`. This style
   is checked with the pipelines on gitlab.com. Ensure that your commits include only
   properly formatted code. One way to comply is to install and use `pre-commit`.
   This package includes the necessary configuration.


8. Commit your changes and push your branch to GitLab::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push

9. Request a review of your merge request through the GitLab website.

Merge Request Guidelines
------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The merge request should work for Python 3.9 to 3.10. Check
   https://gitlab.com/ethz_hvl/hvl_ccb/merge_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

* To run tests from a single file::

    $ py.test tests/test_hvl_ccb.py

  or a single test function::

    $ py.test tests/test_hvl_ccb.py::test_command_line_interface

* If your tests are slow, profile them using the pytest-profiling plugin::

    $ py.test tests/test_hvl_ccb.py --profile

  or for a graphical overview (you need a SVG image viewer)::

    $ py.test tests/test_hvl_ccb.py --profile-svg
    $ open prof/combined.svg

* To add dependency, edit appropriate ``*requirements`` variable in the
  ``setup.py`` file and re-run::

  $ python setup.py develop

* To generate a PDF version of the Sphinx documentation instead of HTML use::

    $ rm -rf docs/hvl_ccb.rst docs/modules.rst docs/_build && sphinx-apidoc -o docs/hvl_ccb && python -msphinx -M latexpdf docs/ docs/_build

  This command can also be run through the make-like shell script::

    $ ./make.sh docs-pdf

  This requires a local installation of a LaTeX distribution, e.g. MikTeX.

Deploying
---------

A reminder for the maintainers on how to deploy.

Make sure all your changes are committed and that all relevant MR are merged. Then switch
to :code:`devel`, update it and create :code:`release-N.M.K` branch::

  $ git switch devel
  $ git pull
  $ git checkout -b release-N.M.K

- Update copyright information (if necessary) in :code:`docs/conf.py` and :code:`README.rst`
- Update or create entry in :code:`HISTORY.rst` (commit message: Update HISTORY.rst: release N.M.K).
- Update, if applicable, :code:`AUTHORS.rst` (commit message: Update AUTHORS.rst: release N.M.K)
- Update features tables in :code:`README.rst` file (commit message: Update README.rst: release N.M.K)
- Update API docs (commit message: Update API-docs: release N.M.K) ::

  $ ./make.sh docs  # windows
  $ make docs  # unix-based-os

Commit all of the above, except for

* :code:`docs/hvl_ccb.dev.picotech_pt104.rst`
* :code:`docs/hvl_ccb.dev.tiepie.base.rst`
* :code:`docs/hvl_ccb.dev.tiepie.channel.rst`
* :code:`docs/hvl_ccb.dev.tiepie.device.rst`
* :code:`docs/hvl_ccb.dev.tiepie.generator.rst`
* :code:`docs/hvl_ccb.dev.tiepie.i2c.rst`
* :code:`docs/hvl_ccb.dev.tiepie.oscilloscope.rst`
* :code:`docs/hvl_ccb.dev.tiepie.utils.rst`.

Before you continue revert the changes in this file.

Then run::

  $ bumpversion patch # possible: major / minor / patch
  $ git push --set-upstream origin release-N.M.K
  $ git push --tags

Go to https://readthedocs.org/projects/hvl-ccb/builds/ and check if RTD docs build for
the pushed tag passed.

Wait for the CI pipeline to finish successfully.

The two following commands are best executed in a WSL or Unix based OS. Run a release check::

  $ make release-check

Finally, prepare and push a release::

  $ make release

Merge the release branch into master and devel branches with :code:`--no-ff` flag and
delete the release branch::

  $ git switch master
  $ git pull
  $ git merge --no-ff release-N.M.K
  $ git push
  $ git switch devel
  $ git merge --no-ff release-N.M.K
  $ git push
  $ git push --delete origin release-N.M.K
  $ git branch --delete release-N.M.K

After this you can/should clean your folder (with WSL/Unix command)::

  $ make clean

Finally, prepare GitLab release and cleanup the corresponding milestone:

1. go to https://gitlab.com/ethz_hvl/hvl_ccb/-/tags/, select the latest release tag,
   press "Edit release notes" and add the release notes (copy a corresponding entry from
   :code:`HISTORY.rst` file with formatting adjusted from ReStructuredText to Markdown);
   press "Save changes";

2. go to https://gitlab.com/ethz_hvl/hvl_ccb/-/releases, select the latest release,
   press "Edit this release" and under "Milestones" select the corresponding milestone;
   press "Save changes";

3. go to https://gitlab.com/ethz_hvl/hvl_ccb/-/milestones, make sure that it is 100%
   complete (otherwise, create a next patch-level milestone and assign it to the
   ongoing Issues and Merge Requests therein); press "Close Milestone".
