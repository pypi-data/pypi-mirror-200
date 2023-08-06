Configuration
=============

Using the command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What will be your best ally in configuring the features is the ``-h`` or ``--help`` option.
This option will show you what can be configured at each stage of the construction of a command.
Start by running the following command:

.. code-block:: bash

   treecker -h

You will then see what you can put after "treecker" in the command line.
Note that the command-line interface (CLI) uses nested subparsers and that the options for a given parser must be placed just after the parser name and before its potential subparsers.
For this reason, until you understand what is going on in the CLI, try to respect the order of the options.

In the previous page we showed how to initialize a tracker with the ``init`` subparser.
If you want to know what options are available for the init subparser, run the ``treecker init -h`` command.
You will discover that there is a ``dir`` option.
This option allows to execute the command in another directory than the current one.
So, to initialize a tracker in a given directory you can run:

.. code-block:: bash

   treecker init --dir <directory-path>

By default, the signature of a file in a snapshot corresponds to the file size.
So if the file size remains the same from one snapshot to the next, the file is considered unchanged.
With the option ``--hash``, Treecker will compute and add a hash value to the tracked file signatures.
If this option is used, the generation time of the snapshot will be strongly lengthened, but it will be possible to detect possible data corruption.

Adding the option ``--hash`` or not when using the ``init`` feature will determine if hash values are computed in future commits.
Adding the option ``--hash`` in when using the ``status`` feature will make Treecker compute the current hash values of the files in the tracked directory and compare them to those saved in the latest snapshot.
The ``--hash`` option cannot be used with the ``status`` feature if Treecker was initialized without hash values.

Using a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

A special configuration can be set up to track a directory.
For this, add a configuration file called ``treecker.conf`` at the root of the tracked directory, that is, next to the ``treecker.json`` file.
It is then possible to choose, among others, which file or directory names will be ignored in the tracking or in the name verification:

.. code-block:: ini

   [treecker.core.naming]
   ignore-patterns = README* LICENSE* CITATION* INSTALL* SETUP* MANIFEST* SOURCES* PKG-INFO Makefile *.php LC_MESSAGES en_US en_GB fr_FR

   [treecker.core.snapshot]
   ignore-patterns = __pycache__ .git

For more configuration options, see the default configuration file `default.conf <https://gitlab.com/dustils/treecker/-/blob/main/src/treecker/default.conf>`_.
