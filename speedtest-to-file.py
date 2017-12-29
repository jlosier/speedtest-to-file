import os
import sys
import time
import json
import csv
from pathlib import Path

# handle arguments
try:
    verbose = sys.argv[1].upper()
    filePath = sys.argv[2]
    fileFormat = sys.argv[2][-4:]
except IndexError:
    print("Cannot run. Improper arguments supplied.\nExample1: $ python *.py <verbose: true/false> <file path>\nExample2: $ python *.py true /home/pi/Documents/speedtest/speedtest.json")
    sys.exit()

if (len(sys.argv) > 2) :
    if (verbose == "TRUE"):
        verbose = True
    else:
        verbose = False

    if ("." in fileFormat):
        fileFormat = "csv"
    else:
        fileFormat = "json"      
else:
    print("Cannot run. Improper arguments supplied.\nExample1: $ python *.py <verbose: true/false> <file path>\nExample2: $ python *.py true /home/pi/Documents/speedtest/speedtest.json")
    sys.exit()

# print message defined in call if verbose == True
def writeMessage (message, verbose) :
    if verbose:
        print(message)
    return;

def writeToJson (results) :
    try:
        with open('/home/pi/Documents/speedtest/speedTestResults.json', 'a') as file:
            json.dump(results, file, sort_keys=True, indent=4)
            file.close()
    except IOError:
        with open('/home/pi/Documents/speedtest/speedTestResults.json', 'w') as newFile:
            json.dump(results, newFile, sort_keys=True, indent=4)
            newFile.close()
    else:
        writeMessage(message = "Results successfully written to json file", verbose = verbose)

def writeToCsv(results, filePath):
    file = Path(filePath)
    headings = ['timestamp','location','ping (ms)','download (Mbit/s)','upload (Mbit/s)']
    
    if (file.exists()):
        try:
            with open(filePath,'a') as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                for data in results:
                    csvWriter.writerow(data)
        except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
        return
    else:
        try:
            with open(filePath,'w') as csvFile:
                csvWriter = csv.DictWriter(csvFile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
                csvWriter.writeheader()
                for data in results:
                    csvWriter.writerow(data)
        except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
        return

# start the test
writeMessage(message = "Performing speed test. Please wait...", verbose = verbose)

speed = os.popen("speedtest-cli").read()

writeMessage(message = "Complete! Here are your results:", verbose = verbose)

if ("Cannot" not in speed):
    # handle the results
    lines = speed.split('\n')

    location = lines[4].split(':')
    ping = location[1].split(' ')
    download = lines[6].split(' ')
    upload = lines[8].split(' ')
        
else:
    # error occurred while running speed test
    writeMessage(message = "There was a problem getting results from speedtest-cli", verbose = verbose)
    location = ["ERROR"]
    ping = ["ERROR", "0"]
    download = ["ERROR", "0"]
    upload = ["ERROR", "0"]

results = [{
        'timestamp' : time.strftime("%Y-%m-%d %X"),
        'location' : location[0],
        'ping' : ping[1], 
        'download' : download[1],
        'upload' : upload[1]
    }]

writeMessage(message = "Timestamp: " + results[0]['timestamp'], verbose = verbose)
writeMessage(message = "Location: " + results[0]['location'], verbose = verbose)
writeMessage(message = "Ping (ms): " + results[0]['ping'], verbose = verbose)
writeMessage(message = "Download (Mbit/s): " + results[0]['download'], verbose = verbose)
writeMessage(message = "Upload (Mbit/s): " + results[0]['upload'], verbose = verbose)

if (fileFormat == "json"):
    writeToJson(results = results)
else:
    writeToCsv(results = results, filePath = filePath)
