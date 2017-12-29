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

def writeToJson (results, filePath) :
    file = Path(filePath)
    
    try:
        if (file.exists()):
            with open(filePath) as read:
                data = json.load(read)

            newJson = []
            for entry in data:
                newJson.append({
                    'timestamp' : entry['timestamp'],
                    'location' : entry['location'],
                    'ping' : entry['ping'],
                    'download' : entry['download'],
                    'upload' : entry['upload']
                })

            newJson.append({
                'timestamp' : results[0]['timestamp'],
                'location' : results[0]['location'],
                'ping' : results[0]['ping'],
                'download' : results[0]['download'],
                'upload' : results[0]['upload']
            })

        
        with open(filePath, 'w') as write:
            json.dump(newJson, write, indent=4)
            write.close()
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))
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
    writeToJson(results = results, filePath = filePath)
else:
    writeToCsv(results = results, filePath = filePath)
