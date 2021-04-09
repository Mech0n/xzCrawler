# xzCrawler

> Save a file for xianzhi. 

### How to Use?

```
.
├── LICENSE
├── README.md
├── crawler.py          # use sqlite to incremental update
├── crawler_set.py      # use python set to incremental update
├── db.py               # sqlite module
├── main.py             # Main script to download all the post
├── requirements.txt
└── xzCrawler-Flask         # Flask Server (Independent part)
    ├── app.py
    ├── crawler_flask.py    # the magically modified crawler to match flask server
    ├── db.py
    ├── index.py            # index module
    ├── indexDoc.py         # index all the post use index module
    ├── main.py
    └── templates
        ├── form.html
        └── search_result.html
```

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

    ![e4368c22b09c10ee45241edbb29764cf.jpg](https://img.vaala.cloud/images/2021/04/09/e4368c22b09c10ee45241edbb29764cf.jpg)

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

### TODO

- support multi key search