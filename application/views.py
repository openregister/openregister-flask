from flask import render_template, request, make_response
from application import app
from .repository import repositories
from thingstance.representations import representations as _representations


# TBD: push this into thingstance.representations ..
representations = {}
for representation in _representations:
    module = __import__('thingstance.representations.' + representation,
                        globals(),
                        locals(),
                        ['content_type'])
    if module.content_type:
        representations[representation] = module


def subdomain(request):
    return request.headers['Host'].split('.')[0]


def render_thing(thing, suffix):
    text = getattr(thing, suffix)
    resp = make_response(text, 200)
    resp.headers['Content-Type'] = representations[suffix].content_type
    return resp


@app.route("/")
def index():
    repository = repositories[subdomain(request)]
    if repository:
        return render_template("repository.html", title=repository.name)

    return render_template('404.html'), 404


@app.route("/<tag>/<hash>")
def thing(tag, hash):
    return thing_suffix(tag, hash, "html")


@app.route("/<tag>/<hash>.<suffix>")
def thing_suffix(tag, hash, suffix):
    repository = repositories[subdomain(request)]
    if repository:
        thing = repository.store.get(hash)
        if thing:
            if suffix == "html":
                return render_template("thing.html",
                                       repository=repository.primitive,
                                       representations=representations,
                                       tag=tag,
                                       hash=hash,
                                       thing=thing.primitive)

            if suffix in representations:
                return render_thing(thing, suffix)

    return render_template('404.html'), 404
