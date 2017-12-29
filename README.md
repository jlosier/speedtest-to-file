# speedtest-to-file
Runs a internet speed test and writes the results to a file (csv or json)

Based off of jgamblin's speed.py gist (https://gist.github.com/jgamblin/3428a164e561baee829c339ac1982e5c)

Requirements:
  1) speedtest-cli is required to use the script (https://pypi.python.org/pypi/speedtest-cli/)
    - speedtest-cli 1.0.7 was used and tested while developing the script
  2) Python's pathlib is required to use the script (https://pypi.python.org/pypi/pathlib/)
    - As of 3.4 pathlib is supposed to be included in Python's libraries however, I am using Python 3.5.3 on a Raspberry Pi and I         had to add the library manually

Usage:
  The script requires two arguments when running the script:
    1) Verbosity (true/false)
        - If you want to view output messages and speed test results in console, add the first argument as "true".
        - If you plan on running the script in a scheduled job and only want to see the results in the file, enter "false" as the             first argument.
    2) File path
        - Should be the full and complete file path plus file name and extension.
        - Supported extensions are .csv and .json (currently in progress)

  Examples:
    $ python speedtest-to-file.py true /home/pi/Documents/speedtests/speedtest.csv
    $ python speedtest-to-file.py false /home/pi/Documents/speedtests/speedtest.json
    
Notes:
  speedtest-cli output:
  index - value
  0 - "Retrieving speedtest.net configuration..."
  1 - Your IP
  2 - "Retrieving speedtest.net server list..."
  3 - "Selecting best server based on ping..."
  4 - <hosted by> (location) [km]: <ping> ms
  5 - "Testing download speed...."
  6 - Download: <dl> Mbit/s
  7 - "Testing upload speed...."
  8 - Upload: <ul> Mbit/s
  9 - *empty*
