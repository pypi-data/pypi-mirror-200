# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_sqs_consumer', 'async_sqs_consumer.test', 'async_sqs_consumer.utils']

package_data = \
{'': ['*']}

install_requires = \
['aioboto3>=10.1.0,<11.0.0',
 'aiobotocore>=2.4.0,<3.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'pyrate-limiter>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'async-sqs-consumer',
    'version': '0.3.4',
    'description': '',
    'long_description': '# Async SQS consumer\n\nPython asynchronous (**async** / **await**) worker for consuming messages\nfrom AWS SQS.\n\nThis is a hobby project, if you find the project interesting\nany contribution is welcome.\n\n## Usage\n\nYou must create an instance of the worker with the url of the queue.\n\nAws credentials are taken from environment variables, you must set the\nfollowing environment variables. Or you can provide a Context object with the\naws credentials `async_sqs_consumer.types.Context`\n\n- `AWS_ACCESS_KEY_ID`\n- `AWS_SECRET_ACCESS_KEY`\n\nExample:\n\nYou can get the queue url with the follow aws cli command\n`aws sqs get-queue-url --queue-name xxxxxx`\n\n```python\n# test_worker.py\n\nfrom async_sqs_consumer.worker import (\n    Worker,\n)\n\nworker = Worker(\n    queue_url="https://sqs.us-east-1.amazonaws.com/xxxxxxx/queue_name"\n)\n\n\n@worker.task("report")\nasync def report(text: str) -> None:\n    print(text)\n\nif __name__: "__main__":\n    worker.start()\n```\n\nNow you can initialize the worker `python test_worker.py`\n\nNow you need to post a message for the worker to process\n\n```python\nimport json\nimport boto3\nimport uuid\n\nclient = boto3.client("sqs")\n\nclient.send_message(\n    QueueUrl="https://sqs.us-east-1.amazonaws.com/xxxxxxx/queue_name",\n    MessageBody=json.dumps(\n        {\n            "task": "report",\n            "id": uuid.uuid4().hex,\n            "args": ["hello world"],\n        }\n    ),\n)\n```\n\nOr you can use aioboto3\n\n```python\nimport asyncio\nimport json\nimport aioboto3\nimport uuid\n\n\nasync def main() -> None:\n    session = aioboto3.Session()\n    async with session.client("sqs") as client:\n        await client.send_message(\n            QueueUrl="https://sqs.us-east-1.amazonaws.com/xxxxxxx/queue_name",\n            MessageBody=json.dumps(\n                {\n                    "task": "report",\n                    "id": uuid.uuid4().hex,\n                    "args": ["hello world"],\n                }\n            ),\n        )\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nTo publish the messages they must have the following structure\n\n```json\n{\n    "type": "object",\n    "properties": {\n        "task": {"type": "string"},\n        "id": {"type": "string"},\n        "args": {"type": "array"},\n        "kwargs": {"type": "object"},\n        "retries": {"type": "number"},\n        "eta": {"type": "string"},\n        "expires": {"type": "string"},\n    },\n    "required": ["task", "id"],\n}\n```\n',
    'author': 'Diego Restrepo',
    'author_email': 'drestrepo@fluidattacks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drestrepom/async_sqs_consumer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
