QuantConnect Utilities
======================

This repo contains various developer resources for the QuantConnect platform. 

Currently, its primary function is to provide version control to the algorithm development process.

## Table of Contents


- [[algolab](algolab.md)] - `algolab.py` - a command line interface for interacting with QC REST API




### Setup

1. Create virtualenv with python3:

        virtualenv -p python3 ~/.virtualenvs/numeris/qctools

2. Start your new virtualenv:

        source ~/.virtualenvs/numeris/qctools/bin/activate

3. Execute Makefile to setup dependencies and run tests:

        make -f Makefile

4. Create `.env` file containing all the required credentials in `.env_example`:
    
        cp .env_example .env
          
   *Note: This creates a copy of* `.env_example` *named* `.env`. *You need modify this file to contain your QuantConnect credentials. Necessary values are found within the* `Api` *section under* `My Account` *on the QuantConnect website. A Project ID (PID) can be obtained by using algolab.py once the account API credentails are configured.* 



---

To learn more about `setup.py`, check out [this repository](https://github.com/kennethreitz/setup.py)


For more info about the sample module used to create this project see [this repository](https://github.com/kennethreitz/samplemod)

