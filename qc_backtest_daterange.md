This script is intended to demonstrate a handful of things we can do with programatic API access to QC. Specifically it performs the following actions:

  1. updates the dates in local params.py to reflect the user’s input
  2. push updates to all existing project files located on QC cloud/website
  3. compiles the project (with new dates in params.py) using the PID located in .env
  4. when compilation is finished trigger backtest of newly compiled project
  5. when backtest is finished print results and download log file
