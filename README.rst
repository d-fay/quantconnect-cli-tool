Ad-hoc Script Utilities
=======================

Repo is intended to contain ad-hoc scripts used for various tasks.

Table of Contents
=================

*List of all scripts contained in this repository*

-----

- **Runner - A reference implementation for python scripts and modules**

  - `[runner] <runner.md>`_ - ``runner.py``

        script to demonstrate calling and interacting with various modules in this repository

-----

- **QuantConnect**

  - `[algolab] <algolab.md>`_ - ``algolab.py``

        a command line interface for interacting with QC REST API


- **TurtleBC**

  - `[turtlebc_insights] <turtlebc_insights.md>`_ - ``turtlebc_insights.py``

        script used for performaning analysis on data scraped from TurtleBC

-----

Usage:
------

1. Create virtualenv with python3:
    ``virtualenv -p python3 ~/.virtualenvs/numeris/scripts``

2. Start your new virtualenv:
    ``source ~/.virtualenvs/numeris/scripts/bin/activate``

3. Execute Makefile to setup dependencies and run tests:
    ``make -f Makefile``

4. Execute a script:
    - Either run one of the scripts listed in the TOC
        ``python algolab.py``
    - Or edit the contents of ``runner.py`` to fit your specific needs then run it!
        ``python runner.py``

------



If you want to learn more about ``setup.py`` files, check out `this repository <https://github.com/kennethreitz/setup.py>`_.



Setup for Quant Connect
=================
You will need to create a copy of `.env_example` and save as `.env`. You will also need to add to it your QuantConnect credentials. These can be found by logging in to QuantConnect and going TO `My Account`. You will see the values you need under the `Api` section.