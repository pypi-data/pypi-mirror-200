Configuration
=============

Using the command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What will be your best ally in configuring the features is the ``-h`` or ``--help`` option.
This option will show you what can be configured at each stage of the construction of a command.
Start by running the following command:

.. code-block:: bash

   pashword -h

You will then see what you can put after "pashword" in the command line.
Note that the command-line interface (CLI) uses nested subparsers and that the options for a given parser must be placed just after the parser name and before its potential subparsers.
For this reason, until you understand what is going on in the CLI, try to respect the order of the options.

In the previous page we showed how to read a password book with the ``read`` subparser.
If you want to know what options are available for the read subparser, run the ``pashword read -h`` command.
You will discover that there are a few options, including ``--hash``.
This option allows you to be notified when you mistype your secret key.
Use option ``--hash``, followed by the path to the file in which a hash value of your secret key will be stored:

.. code-block:: bash

   pashword read your-name.conf --hash your-name.json

If the file does not exist, it will be generated with the value of the secret key that you will enter to decode your passwords.
When the file already exists, it is used to compare the secret key you enter with the one you entered the first time.
If you want to change your secret key, simply delete the file containing the hash.

Using a configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

Everything that can be configured via the CLI can also be configured from a configuration file.
The default configuration of the package is defined in the `default.conf <https://gitlab.com/dustils/pashword/-/blob/main/src/pashword/default.conf>`_ file.
The easiest way to create your own configuration file is to copy this file and modify its content.

Let's now assume that you have named your own configuration file ``custom.conf``.
To get the same result as before without specifying the option in the command line, specify a value to the ``hash`` entry in the ``pashword.main.read`` section of the configuration file and run:

.. code-block:: bash

   pashword --config custom.conf read your-name.conf

It is not necessary to keep all the sections in the configuration file.
You can delete all the sections and options you have not modified.
If you look at the structure of the package, you will notice that the names of the sections correspond to the names of the modules to which the options are attached.
