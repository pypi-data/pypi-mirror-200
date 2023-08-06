Vanilla example
===============

Treecker contains a default configuration of almost all parameters.
You will see later how to use the command-line interface or your own configuration file to replace the default values.
For now, and thanks to all the preconfigured parameters, you will be able to test the package features with a minimum of effort.

Initialize tracking
~~~~~~~~~~~~~~~~~~~

To initialize a tree tracker in a directory, run the following command.
This will create a file named ``treecker.json`` in the directory to track.

.. code-block:: bash

   treecker init --hash

Display changes
~~~~~~~~~~~~~~~

To display the changes made since the last snapshot, execute the following command.

.. code-block:: bash

   treecker status --hash

Save changes
~~~~~~~~~~~~

To save the change displayed in the status, run the following command.
This will overwrite the ``treecker.json`` file.

.. code-block:: bash

   treecker commit

Display issues
~~~~~~~~~~~~~~

To display incorrectly nammed files and directories, execute the following command.

.. code-block:: bash

   treecker issues
