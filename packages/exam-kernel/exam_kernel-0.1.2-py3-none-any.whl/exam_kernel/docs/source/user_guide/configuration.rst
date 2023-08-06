Exam Kernel Configuration
=========================

All configuration is set in the ``ipython_config.py``. To find out where this file is located please visit `the Ipython docs <https://ipython.readthedocs.io/en/stable/config>`_.

Terminal Commands
-----------------

``block_terminal_commands`` is used for blocking any commands preceded by ``!`` will be blocked (e.g. ``!ls``). This is ``True`` by default.

Example::

    # In ipython_config.py
    # Allow the use of commands preceded by an exclamation mark
    c.ExamKernel.block_terminal_commands = False

Initialization Code
-------------------

``init_code`` is used for executing code whenever the kernel is fully loaded.

Example::

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.init_code = """
    import random as rd
    from math import sqrt

    def my_fun(x):
        return x**2
    """

In the above example, the library ``random`` will always be imported under the name ``rd``. The function ``my_fun`` will be available after starting the kernel.

Imports
-------

There are two ways to configure how imports are blocked or allowed.

* ``allowed_imports`` - Takes a list of module names. If this option is set, only imports in this list can be imported
* ``blocked_imports`` - Takes a list of module names. If this option is set, all inputs specified are blocked. If ``allowed_imports`` is set, ``blocked_imports`` will be ignored.

Example of using ``allowed_imports``::

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.allowed_imports = ["math", "random"]

.. code-block:: python
    :caption: Example of trying to import a module that is not in the allowed imports

    import os
    ---------------------------------------------------------------------------
    ModuleNotFoundError: No module named os or os blocked by kernel.
    Allowed imports are: [math, random]
    

Example of using ``blocked_imports``::

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.blocked_imports = ["os", "pandas"]

.. code-block:: python
    :caption: Example of trying to import a module that is in the blocked imports

    import os
    ---------------------------------------------------------------------------
    ModuleNotFoundError: No module named os or os blocked by kernel.
    The following imports are blocked: [os, pandas]

Magic Commands
--------------

There are two ways to configure how both line and cell magic commands (e.g. ``%%time``) are blocked or allowed.

* ``allowed_magics`` - Takes a list of magic names. If this option is set, only magics in this list can be used
* ``blocked_magicss`` - Takes a list of magic names. If this option is set, all magics specified are blocked. If ``allowed_magics`` is set, ``blocked_magics`` will be ignored.

Example of using ``allowed_magics``::

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.allowed_imports = ["time"]

.. code-block:: python
    :caption: Example of trying to use a magic that is not in the allowed magics

    %timeit my_fun()
    ---------------------------------------------------------------------------
    ValueError: No magic named timeit or timeit blocked by kernel.
    Allowed magics are: [time]

Example of using ``blocked_magics``::

    # In ipython_config.py
    c = get_config()
    c.ExamKernel.blocked_imports = ["time"]

.. code-block:: python
    :caption: Example of trying to use a magic that is in the blocked magics

    %%time
    ---------------------------------------------------------------------------
    ValueError: No magic named time or time blocked by kernel.
    The following magics are blocked: [time]