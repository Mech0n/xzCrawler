from __future__ import unicode_literals

from concurrent.futures import ThreadPoolExecutor
from os import makedirs, remove
from os.path import exists

from jieba.analyse import ChineseAnalyzer
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter


class Index:
    def __init__(self):
        self.indexdir = "SearchIndex/IndexBak"

        self.analyzer = ChineseAnalyzer()
        self.schema = Schema(
            title=TEXT(stored=True),
            path=ID(stored=True),
            content=TEXT(stored=True, analyzer=self.analyzer),
        )

        if not exists(self.indexdir):
            makedirs(f"./{self.indexdir}")
            self.ix = create_in(self.indexdir, self.schema)

        else:
            self.ix = open_dir(self.indexdir)

    # index one content
    def write(self, title, path, content):
        try:
            # writer = AsyncWriter(self.ix, delay=0.25)
            writer = self.ix.writer()
            writer.add_document(title=title, path=path, content=content)
            writer.commit()
            print(path)

        except Exception as e:
            print(f"[ERROR] Index.write : {str(e)}")

    # search from index
    def search(self, querystring):
        """
        querystring : string
        return : [
            {
                content : balabala
                path : balabala
                title : balaba
                highlight : balabala
            }
        ]
        """
        try:
            parser = QueryParser("content", self.ix.schema)
            query = parser.parse(querystring)

            res = []
            with self.ix.searcher() as searcher:
                for hit in searcher.search(query, limit=None):
                    hit_element = {}
                    hit_element = dict(hit)
                    hit_element["highlight"] = hit.highlights("content")
                    res.append(hit_element)
                    # print(f"[INFO] Index.search : {hit_element}")
            return res
        except Exception as e:
            print(f"[ERROR] Index.search : {e}")


if __name__ == "__main__":

    idx = Index()

    title = "First document"
    path = ("/a",)
    content = "This is the first document we've added!"

    # The experience of using multithreading is not good

    # t = ThreadPoolExecutor(20)
    # for i in range(100):
    # t.submit(idx.write, title, f"/{i}", content)
    # t.shutdown(wait=True)

    # for i in range(100):
    # idx.write(title, f"/{i}", content)

    for i in idx.search("登陆路径"):
        print(i["path"])
        print(i["highlight"])
