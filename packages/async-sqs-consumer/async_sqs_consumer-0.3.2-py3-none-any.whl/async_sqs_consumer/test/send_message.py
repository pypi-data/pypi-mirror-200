import boto3
import json
import uuid

client = boto3.client("sqs", region_name="us-east-1")

for _ in range(1):
    client.send_message(
        QueueUrl=(
            "https://sqs.us-east-1.amazonaws.com/205810638802/integrates_tasks_dev"
        ),
        MessageBody=json.dumps(
            {
                "id": uuid.uuid4().hex,
                "task": "clone",
                "args": [
                    "vergeladc",
                    "ddafdd56-c17f-43c3-9e4c-7e3e074399b9",
                ],
            }
        ),
    )
