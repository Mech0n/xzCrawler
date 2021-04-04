from concurrent.futures import ThreadPoolExecutor
from crawler import crawler

# url = f"https://xz.aliyun.com/t/{str(i)}"


def htmls():
    c = crawler()
    pool = ThreadPoolExecutor(20)
    for idx in range(10, 9396):
        pool.submit(c.crawler, f"https://xz.aliyun.com/t/{str(idx)}")
    pool.shutdown(wait=True)


if __name__ == "__main__":
    htmls()
