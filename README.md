This is a simple script to retrieve a list of all contacts from a Constant Contact account and output them in CSV format.

As of April 2012 this works even on expired Constant Contact accounts. You will need to [obtain a Constant Contact API key](http://community.constantcontact.com/t5/Documentation/API-Keys/ba-p/25015) which is obtainable even for expired accounts.

Required Python libraries:

* [httplib2](http://code.google.com/p/httplib2/) -- `pip install httplib2`

Usage:

    getcontacts.py [options] <cc_api_key> <cc_username> <cc_password> [csv_file]

      cc_api_key            Your Constant Contact API key
      cc_username           Your Constant Contact account username
      cc_password           Your Constant Contact account password
      csv_file              Filename to write CSV data to (uses stdout if omitted)

    Options:
      -h, --help            show this help message and exit
      -n, --noprogress      don't print progress messages to stdout
