import boto3
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize AWS clients
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

# Specify your S3 bucket and prefix
bucket_name = 'sagemaker-ap-northeast-1-133132895539'
subdir = 'whisper/input'

# Specify your Lambda function name
lambda_function_name = 'whisperSageMaker'

# Fetch audio files from S3
audio_objects = s3_client.list_objects(Bucket=bucket_name, Prefix=subdir)['Contents']

# Function to invoke lambda
def invoke_lambda(audio_object_key):
    event = {
        'audio_object_key': audio_object_key
    }
    
    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='Event',  # Use 'Event' for asynchronous invocation, 'RequestResponse' for synchronous
        Payload=json.dumps(event)
    )
    return response

# Create a ThreadPoolExecutor
max_workers = 10
num_repeat = 10
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use a list comprehension to create a list of futures
    # Invoke the lambda function 10 times for each audio file
    futures = [executor.submit(invoke_lambda, audio_object['Key']) for _ in range(num_repeat) for audio_object in audio_objects]

    # As each future completes, print the returned result (in this case, the response from the Lambda function)
    for future in as_completed(futures):
        try:
            print(future.result())
        except Exception as exc:
            print(f'An exception occurred: {exc}')
