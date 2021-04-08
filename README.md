# xzCrawler

> Save a file for xianzhi. 

### How to Use?

#### Just Use Crawler
⚠️: Change the range in `main.py` first.

- pip install the requirments.
    ```shell
    pip install -r requirements.txt
    ```
- Run the script and all the htmls in `doc`
    ```shell
    python main.py
    ```

#### Flask Extend

- `cd xzCrawler-Flask`

- Run `main.py` use the another crawler(`crawler_flask.py`)

- Index all html, result will be stored in `SearchIndex` or the path you chose.
    ```shell
    python indexDoc.py
    ```
    
- Run Flask Server

    ```shell
    python app.py
    ```

    

### Features

- Incremental update
    
    - Python sqlite : `database.db` stores the requested past-url
    
- Index(Flask Extend)

    > A simple index script, Implemented by adding content sequentially, a strong script will coming soon😝.

    - `Whoosh`
    - `Jieba`

- Main site

    > A simple main site just provide a search bur.

    - search
