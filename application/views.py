from flask import render_template, request, make_response, Markup
from application import app
from .registry import registers
from thingstance.representations import representations as _representations


# TBD: register url should be constructed from the register object ..
def register_filter(register):
    result = ('<a href="%s.thingstance.dev"'
              ' class="register">%s</a>' % (register, register))
    return Markup(result)


# TBD: should be a register of filters for a Field/Datatype ..
@app.template_filter('datatype')
def datatype_filter(value, fieldname):
    if fieldname == "register":
        return register_filter(value)
    elif fieldname == "hash":
        return Markup('<a href="/hash/%s">%s</a>' % (value, value))
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


@app.route("/hash/<hash>")
def thing_by_hash(hash):
    return thing_by_hash_suffix(hash, "html")


@app.route("/hash/<hash>.<suffix>")
def thing_by_hash_suffix(hash, suffix="html"):
    register = None
    try:
        register = registers[subdomain(request)]
        thing = register._store.get(hash)
        if thing:
            if suffix == "html":
                return render_template("thing.html",
                                       register=register.primitive,
                                       representations=representations,
                                       hash=hash,
                                       thing=thing.primitive)

            if suffix in representations:
                return represent_thing(thing, suffix)
    except KeyError:
        pass

    return render_template('404.html', register=register), 404


@app.route("/")
def things():
    return find_things("Thing", query={})


@app.route("/name/<name>")
def find_latest_thing_by_name(name):
    return find_latest_thing(query={"name": name})


def find_latest_thing(query={}, suffix="html"):
    register = registers[subdomain(request)]
    meta, things = register._store.find(query)
    thing = things[0]  # egregious hack to find latest ..
    return thing_by_hash_suffix(thing.hash, "html")


def find_things(tag, query={}, suffix="html"):
    register = None
    try:
        register = registers[subdomain(request)]
        meta, things = register._store.find(query)
        things_list = [[thing.hash, thing.primitive] for thing in things]
        thing_keys = []
        if things_list:
            thing_keys = [field for field in things_list[0][1]]
            thing_keys.remove('register')
            thing_keys.remove('name')
            thing_keys.sort()
        if suffix == "html":
            return render_template("things.html",
                                   register=register.primitive,
                                   representations=representations,
                                   meta=meta,
                                   things_list=things_list,
                                   thing_keys=thing_keys)

    except KeyError:
        pass

    return render_template('404.html', register=register), 404
