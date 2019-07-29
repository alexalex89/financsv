# FinanCSV

A simple parser to get an overview on how you spent your money. Receives payment data in _CSV-MT940-Format_ and payment receiver/sender names in YAML format as input.

Example call:

`python3 financsv.py -i /home/user/transactions.csv -r /home/user/receivers.yml`

Python3.7 or higher required.

Work in progress.

## TODO

* Refactoring
* Support other formats
* Visualization
* Some kind of AI interpreting the payments
