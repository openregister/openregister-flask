from flask import render_template, request
from application import app
from .repository import repositories


def subdomain(request):
    return request.headers['Host'].split('.')[0]


@app.route("/")
def index():
    repository = repositories[subdomain(request)]

    if repository:
        return render_template("repository.html", title=repository.name)

    return render_template('error.html'), 404


@app.route("/<tag>/<hash>")
def thing(tag, hash):
    repository = repositories[subdomain(request)]

    if repository:
        thing = repository.store.get(hash)

        if thing:
            return render_template("thing.html",
                                   repository=repository.primitive,
                                   title=repository.name + " ☞ " + tag,
                                   hash=hash,
                                   thing=thing.primitive)

    return render_template('error.html'), 404
