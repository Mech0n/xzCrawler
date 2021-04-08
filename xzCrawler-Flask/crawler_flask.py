import pickle
from os import makedirs, remove
from os.path import abspath, basename, dirname, exists

import requests
from bs4 import BeautifulSoup
from rich import print

from db import db


class crawler:
    def __init__(self):
        self.baseurl = "https://xz.aliyun.com/"

        # main directory
        self.basedir = "static"
        # image directory
        self.imgdir = "img"
        self.htmldir = "templates/doc"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0"
        }

        self.database = db()

        if not exists(self.basedir):
            makedirs(f"./{self.basedir}")

    def check_and_add(self, idx):
        try:
            url = f"https://xz.aliyun.com/t/{str(idx)}"
            query_res = self.database.query((idx,))

            if len(query_res) != 0 and query_res[0]["id"] == idx:
                print(f"[bold yellow][INFO][/bold yellow] {url} exists")
                return True
            else:
                # self.database.add((idx, url, False))
                return False
        except Exception as e:
            print(f"check_and_add : {e}")

    # Download engine
    def download(self, url, sess, path):
        print(f"[bold yellow][INFO][/bold yellow]Downloading {url} to {path}")

        if exists(path):
            return

        if not exists(dirname(path)):
            makedirs(dirname(path))

        with open(path, "wb") as file:
            try:
                res = sess.get(url, timeout=5)

                # TODO: boom
                if res.status_code != 200:
                    print(
                        f"[bold red][Failed][/bold red]status_code : {res.status_code} while downloading {url} to {path}"
                    )

                    return
                
                file.write(res.content)

            except:
                print(
                    f"[bold red][Failed][/bold red] cannot establish connection while downloading {url} to {path}"
                )


    def crawler(self, idx):
        url = f"https://xz.aliyun.com/t/{str(idx)}"
        # add url in set
        if self.check_and_add(idx):
            return

        print(f"[bold yellow][INFO][/bold yellow]Downloading {url}")
        with requests.session() as sess:
            sess.headers.update(self.headers)

            res = sess.get(url)

            # TODO: boom
            if res.status_code != 200:
                print(
                    f"[bold red][Failed][/bold red] status_code : {res.status_code} while downloading {url}"
                )
                return

            soup = BeautifulSoup(res.content.decode("utf-8"), features="html.parser")

            # get title
            title = None
            title = soup.find_all("title")[0].get_text()

            # TODO: boom
            if title is None:
                print(f"[bold red][Failed][/bold red]No title while downloading {url}")
                return False

            if exists(f"./{self.basedir}/{title}.htm"):
                return

            # self.database.add((idx, title, False))

            # Process static files
            for link in soup.find_all("link"):
                ln = link["href"].lstrip("/")
                url = self.baseurl + ln
                # path = f"./{self.basedir}/{ln}"
                path = f"./{ln}"
                self.download(url, sess, path)

                # TODO
                if "static/" in ln:
                    local_ln = "{{ url_for('static', " + f"filename='{ln[7:]}" + "') }}"
                else:
                    local_ln = "{{ url_for('static', " + f"filename='{ln}" + "') }}"
                # {{url_for('static', filename='ayrton_senna_movie_wallpaper_by_bashgfx-d4cm6x6.jpg')}}
                link["href"] = local_ln

            # Process images
            for image in soup.find_all("img"):
                ln = image["src"]
                if ln.startswith("/static"):
                    n = link["href"].lstrip("/")
                    url = self.baseurl + ln
                    path = f"./{self.basedir}/{ln}"
                    self.download(url, sess, path)

                    # local_ln = f"./{ln}"
                    # TODO
                    local_ln = "{{ url_for('static', " + f"filename='{ln[7:]}" + "') }}"
                    image["src"] = local_ln

                path = None
                local_ln = None

                if ln.startswith("https://"):
                    path = f"./{self.basedir}/{self.imgdir}/{ln[8:]}"
                    local_ln = f"{self.imgdir}/{ln[8:]}"
                    local_ln = (
                        "{{ url_for('static', " + f"filename='{local_ln}" + "') }}"
                    )

                if ln.startswith("http://"):
                    path = f"./{self.basedir}/{self.imgdir}/{ln[7:]}"
                    local_ln = f"{self.imgdir}/{ln[7:]}"
                    local_ln = (
                        "{{ url_for('static', " + f"filename='{local_ln}" + "') }}"
                    )

                if path is not None and local_ln is not None:
                    self.download(ln, sess, path)
                    image["src"] = local_ln

            path = f"./{self.htmldir}/{title}.htm"

            if exists(path):
                return

            if not exists(dirname(path)):
                makedirs(dirname(path))

            with open(path, "w") as file:
                file.write(soup.prettify())

            self.database.add((idx, title, False))



if __name__ == "__main__":
    c = crawler()
    c.crawler(400)
