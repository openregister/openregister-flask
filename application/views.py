from flask import render_template, request, make_response, Markup
from application import app
from .repository import repositories
from thingstance.representations import representations as _representations


@app.template_filter('tags')
def tags_filter(tags):
    result = ['<a href="/%s" class="tag">%s</a>' % (tag, tag) for tag in tags]
    return Markup(result)

@app.template_filter('datatype')
def datatype_filter(value, fieldname):
    if fieldname == "tags":
        return tags_filter(value)
    elif fieldname == "registers":
        return tags_filter(value)
    elif fieldname == "hash":
        return Markup('<a href="/Thing/%s">%s</a>' % (value, value))
    return value


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


def represent_thing(thing, suffix):
    text = getattr(thing, suffix)
    resp = make_response(text, 200)
    resp.headers['Content-Type'] = representations[suffix].content_type
    return resp


@app.route("/")
def index():
    try:
        repository = repositories[subdomain(request)]
        return render_template("thing.html",
                               repository=repository.primitive,
                               tag="Registry",
                               hash=repository.hash,
                               thing=repository.primitive)
    except KeyError:
        return render_template('404.html'), 404


@app.route("/<tag>/<hash>")
def thing(tag, hash):
    return thing_suffix(tag, hash, "html")


@app.route("/<tag>/<hash>.<suffix>")
def thing_suffix(tag, hash, suffix="html"):
    try:
        repository = repositories[subdomain(request)]
        thing = repository._store.get(hash)
        if thing:
            if suffix == "html":
                return render_template("thing.html",
                                       repository=repository.primitive,
                                       representations=representations,
                                       tag=tag,
                                       hash=hash,
                                       thing=thing.primitive)

            if suffix in representations:
                return represent_thing(thing, suffix)
    except KeyError:
        pass

    return render_template('404.html', tag=tag), 404


@app.route("/Thing")
def things():
    return find_things("Thing", query={})


@app.route("/<tag>")
def tag(tag):
    return find_things(tag, query={"tags":tag})


def find_things(tag, query={}, suffix="html"):
    try:
        repository = repositories[subdomain(request)]
        meta, things = repository._store.find(query)
        things_list = [[thing.hash, thing.primitive] for thing in things]
        if suffix == "html":
            return render_template("things.html",
                                   repository=repository.primitive,
                                   representations=representations,
                                   tag=tag,
                                   meta=meta,
                                   things_list=things_list)

    except KeyError:
        pass

    return render_template('404.html', tag=tag), 404
