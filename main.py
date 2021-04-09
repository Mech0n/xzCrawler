from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from traceback import format_exc

from crawler import crawler

# url = f"https://xz.aliyun.com/t/{str(i)}"


class ThreadPool:
    def __init__(self, num_of_threads: int) -> None:
        self.thread_pool_executor = ThreadPoolExecutor(num_of_threads)

        self.worker_queue = Queue(num_of_threads)
        for i in range(num_of_threads):
            worker = crawler()
            self.worker_queue.put(worker)

    def __del__(self):
        self.thread_pool_executor.shutdown(wait=True)

    def submit(self, idx):
        self.thread_pool_executor.submit(self.run, idx)

    def run(self, idx) -> None:
        try:
            worker = self.worker_queue.get(block=True)  # wait until a worker is available
            worker.crawler(idx)
            self.worker_queue.put(worker)
        except Exception as e:
            print(
                f"[Failed] crawler thread: {e}",
            )
            print(format_exc())


if __name__ == "__main__":
    t = ThreadPool(20)

    for i in range(9350, 9395):
        t.submit(i)
