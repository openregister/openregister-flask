from flask import (
    render_template,
    request,
    make_response,
    Markup,
    abort,
    current_app
)
from application import app, db
from .registry import registers, Register
from thingstance.representations import representations as _representations


def link(register, field, value):
    return ('<a href="http://%s.%s/%s/%s">%s</a>'
            % (register, app.config['REGISTER_DOMAIN'], field, value, value))


# TBD: should be a register of filters for a Field/Datatype ..
@app.template_filter('datatype')
def datatype_filter(value, fieldname):
    if fieldname == "sameAs":
        return Markup('<a href="%s">%s</a>' % (value, value))
    if fieldname == "hash":
        return Markup('<a href="/hash/%s">%s</a>' % (value, value))
    if fieldname == "address":
        return Markup(link("address", "hash", value))
    if fieldname == "field":
        return Markup(link("field", "name", value))
    if fieldname == "addressCountry":
        return Markup(link("country", "addressCountry", value))
    if fieldname == "register":
        return Markup(link("register", "name", value))
    if fieldname == "fields":
        return Markup([link('field', 'name', v) for v in value])
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
    subdomain = request.headers['Host'].split('.')[0]
    if '-' in subdomain:
        return subdomain.split('-')[0]
    else:
        return subdomain


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
    register_name = subdomain(request)
    register = find_or_initalise_register(register_name)
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
    else:
        abort(404)


@app.route("/")
def things():
    return find_things("Thing",
                       query={},
                       page=int(request.args.get('page', 1)))


@app.route("/name/<value>")
def find_latest_thing_by_name(value):
    return find_latest_thing(query={"name": value})


@app.route("/addressCountry/<value>")
def find_latest_thing_by_addressCountry(value):
    return find_latest_thing(query={"addressCountry": value})


def find_latest_thing(query={}, suffix="html"):
    register_name = subdomain(request)
    register = find_or_initalise_register(register_name)
    meta, things = register._store.find(query)
    thing = things[0]  # egregious hack to find latest ..
    return thing_by_hash_suffix(thing.hash, "html")


def find_things(tag, query={}, suffix="html", page=None):
    register_name = subdomain(request)
    register = find_or_initalise_register(register_name)

    if not page:
        page = 1
    meta, things = register._store.find(query, page)

    things_list = [[thing.hash, thing.primitive] for thing in things]
    thing_keys = []
    if things_list:
        thing_keys = [field for field in things_list[0][1]]
        # TBD: order by field names in the register
        thing_keys.sort()
        if "name" in thing_keys:
            thing_keys.remove("name")
            thing_keys = ["name"] + thing_keys
    if suffix == "html":
        return render_template("things.html",
                               register=register.primitive,
                               representations=representations,
                               meta=meta,
                               things_list=things_list,
                               thing_keys=thing_keys)


def find_or_initalise_register(register_name):
    if not registers.get(register_name):
        collections = db.collection_names()
        if register_name not in collections:
            return abort(404)
        registers[register_name] = Register(register_name,
                                            current_app.config['MONGO_URI'])
    return registers.get(register_name)
