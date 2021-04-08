from flask import Flask, render_template, request, redirect, url_for
from index import Index

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def form():
    return render_template("form.html")


@app.route("/search_result", methods=["GET", "POST"])
def search_result():
    if request.method == 'POST':
        search_key = request.form['key']
        idx = Index()
        # TODO : split search_list
        search_list = idx.search(search_key)
        return render_template("search_result.html", results=search_list, search_len= len(search_list))

@app.route("/doc/<path>")
def doc(path):
    try:
        return render_template(f"/doc/{path}")
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()
