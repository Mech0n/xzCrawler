from os.path import exists

from bs4 import BeautifulSoup

from db import db
from index import Index


class IndexDoc:
    def __init__(self):
        self.basedir = "templates/doc"
        self.database = db()
        self.index = Index()
        self.errorset = set()

    def __del__(self):
        print(self.errorset)

    def index_all(self):
        try:
            for element in self.database.query_all_new_content():

                path = f"./{self.basedir}/{element['title']}.htm"
                if not exists(path):
                    print(f"[ERROR] IndexDoc.index_all : {path}.html , No such file.")
                    continue
                with open(path, "r") as file:
                    html = file.read()
                soup = BeautifulSoup(html, features="html.parser")
                tags = soup.find_all("pre")
                for tag in tags:
                    tag.decompose()
                body = soup.find_all(class_="topic-content markdown-body")
                if len(body) > 0:
                    content = body[0].get_text()
                else:
                    self.errorset.add(path)
                    print(f"[ERROR] IndexDoc.index_all : {path} have no content")
                    continue
                # self.index.write(element["title"], path, content)
                self.index.write(element["title"], f"{element['title']}.htm", content)
                self.database.indexed((True, element["id"]))
        except Exception as e:
            print(f"[ERROR] IndexDoc.index_all : {e}")


if __name__ == "__main__":
    idoc = IndexDoc()
    idoc.index_all()
