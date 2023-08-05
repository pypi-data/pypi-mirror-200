from async_sqs_consumer.queue import (
    Queue,
)
from async_sqs_consumer.worker import (
    Worker,
)
from asyncio import (
    sleep,
)

worker = Worker(
    queues={
        "default": Queue(
            url="https://sqs.us-east-1.amazonaws.com/205810638802/integrates_tasks_dev"
        )
    },
    max_workers=10,
)


@worker.task("report", queue_name="default")
async def report(text: str) -> None:
    print(text)
    await sleep(5)
    print("finish task")


if __name__ == "__main__":
    worker.start()
