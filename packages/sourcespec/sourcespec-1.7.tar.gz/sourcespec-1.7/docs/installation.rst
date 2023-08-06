############
Installation
############

SourceSpec requires at least Python 3.6. All the required dependencies
will be downloaded and installed during the setup process.


Installing the latest release
-----------------------------

Using pip and PyPI (preferred method)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The latest release of SourceSpec is available on the `Python Package
Index <https://pypi.org/project/sourcespec/>`__.

You can install it easily through ``pip``:

::

   pip install sourcespec

From SourceSpec GitHub releases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the latest release from the `releases
page <https://github.com/SeismicSource/sourcespec/releases>`__, in
``zip`` or ``tar.gz`` format, then:

::

   pip install sourcespec-X.Y.zip

or

::

   pip install sourcespec-X.Y.tar.gz

Where, ``X.Y`` is the version number (e.g., ``1.2``). You don’t need to
uncompress the release files yourself.


Installing a developer snapshot
-------------------------------

If you need a recent feature that is not in the latest release (see the
``unreleased`` section in `CHANGELOG
<https://github.com/SeismicSource/sourcespec/blob/master/CHANGELOG.md>`__),
you want to use the more recent development snapshot from the `SourceSpec
GitHub repository <https://github.com/SeismicSource/sourcespec>`__.

Using pip (preferred method)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install the most recent development snapshot is to download
and install it through ``pip``, using its builtin ``git`` client:

::

    pip install git+https://github.com/SeismicSource/sourcespec.git

Run this command again, from times to times, to keep SourceSpec updated with
the development version.

Cloning the SourceSpec GitHub repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to take a look at the source code (and possibly modify it 😉),
clone the project using ``git``:

::

    git clone https://github.com/SeismicSource/sourcespec.git

or, using SSH:

::

    git clone git@github.com:SeismicSource/sourcespec.git

(avoid using the "Download ZIP" option from the green "Code" button, since
version number is lost).

Then, go into the ``sourcespec`` main directory and install the code in
"editable mode" by running:

::

    pip install -e .

You can keep your local SourceSpec repository updated by running ``git pull``
from times to times. Thanks to ``pip``'s "editable mode", you don't need to
reinstall SourceSpec after each update.
