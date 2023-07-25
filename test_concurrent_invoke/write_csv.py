import boto3
import csv
from datetime import datetime, timedelta
from dateutil import parser

# Assume these are your start and end times in 'YYYY-MM-DD HH:MM:SS' format
start_time_str = '2023-07-19 15:00:00' # Tokyo Time
end_time_str = '2023-07-21 00:00:00'

# Convert to Unix timestamp (milliseconds)
startTime = int(parser.parse(start_time_str).timestamp() * 1000)
endTime = int(parser.parse(end_time_str).timestamp() * 1000)


def get_log_events(logGroupName, startTime, endTime):
    cloudwatch = boto3.client('logs')

    # Initialize events list and next_token
    events = []
    next_token = None

    while True:
        if next_token:
            response = cloudwatch.filter_log_events(
                logGroupName=logGroupName,
                startTime=startTime,
                endTime=endTime,
                nextToken=next_token
            )
        else:
            response = cloudwatch.filter_log_events(
                logGroupName=logGroupName,
                startTime=startTime,
                endTime=endTime
            )

        # Parse response and append to events
        for event in response['events']:
            message = event['message']
            if 'CSV_INFO' in message:
                _, audio_file_name, transcription, duration, start_time, end_time = message.split(',')
                events.append((audio_file_name, transcription, duration, start_time, end_time))

        # Check for next_token
        if 'nextToken' in response:
            next_token = response['nextToken']
        else:
            break

    return events




def write_to_csv(filename, rows):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["audio file name", "transcription", "duration", "start time", "end time"])
        writer.writerows(rows)

if __name__ == "__main__":
    logGroupName = '/aws/lambda/whisperSageMaker'
    filename = 'test_concurrent_invoke/transcriptions.csv'

    events = get_log_events(logGroupName, startTime, endTime)
    write_to_csv(filename, events)
