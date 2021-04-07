# xzCrawler

> Save a file for xianzhi. 

### How to Use?

#### Crawler
⚠️: Change the range in `main.py` first.

- pip install the requirments.
    ```shell
    pip install -r requirements.txt
    ```
- Run the script.
    ```shell
    python main.py
    ```

#### Index

- Run Crawler

- Index all html, result will be stored in `SearchIndex` or the path you chose.
    ```shell
    python indexDoc.py
    ```

### Features

- Incremental update
    - Python sqlite : `database.db` stores the requested past-url

### TODO

- Main site
    - search
- Index
    > A simple index script, Implemented by adding content sequentially, a strong script will coming soon😝.
    - `Whoosh`
    - `Jieba`