from flask import (
    render_template,
    request,
    make_response,
    Markup,
    abort,
    current_app,
    flash,
    redirect,
    url_for
)
from application import app, db
from .registry import registers, Register
from thingstance.representations import representations as _representations
from .utils import log_traceback


def link(register, field, value):
    return ('<a href="http://%s.%s/%s/%s">%s</a>'
            % (register, app.config['REGISTER_DOMAIN'], field, value, value))


# TBD: should be a register of filters for a Field/Datatype ..
@app.template_filter('datatype')
def datatype_filter(value, fieldname):

    # datatypes
    if fieldname == "sameAs":
        return Markup('<a href="%s">%s</a>' % (value, value))
    if fieldname == "hash":
        return Markup('<a href="/hash/%s">%s</a>' % (value, value))
    if fieldname == "name":
        return Markup('<a href="/name/%s">%s</a>' % (value, value))

    # link by hash
    if fieldname == "address":
        return Markup(link("address", "hash", value))

    # link by name
    if fieldname == "addressCountry":
        return Markup(link("country", "addressCountry", value))
    if fieldname == "register":
        return Markup(link("register", "register", value))
    if fieldname == "field":
        return Markup(link("field", "field", value))
    if fieldname == "fields":
        return Markup([link('field', 'field', v) for v in value])

    return value


@app.template_filter('thousands_comma')
def thousands_comma_filter(value):
    if value:
        return "{:,d}".format(value)
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

@app.route("/search")
def search():
    #fake data for now
    register_name = {'name' : subdomain(request)}
    return render_template('search.html', register=register_name)

# TODO - protect urls like this
@app.route("/load-data")
def load_data():
    '''
        This loads data for a register repository
        e.g. https://github.com/openregister/registername.register.

        It will then load the data contained in the repository and
        load it into the register. Currently that means loading the data
        into the mongodb for the register.
    '''
    register_name = subdomain(request)
    register = registers.get(register_name)
    try:
        if not register:
            register = Register(register_name.capitalize(),
                                current_app.config['MONGO_URI'])
            registers[register_name] = register
        zip_url = '%s/%s.register/archive/master.zip' % (current_app.config['GITHUB_ORG'], register_name)
        register.load_remote(zip_url)
        flash('Loaded data into register')
    except Exception as ex:
        log_traceback(current_app.logger, ex)
        flash('Problem loading data into register', 'error')

    return redirect(url_for('things'))


@app.route("/<key>/<value>")
def find_latest_thing_by_addressCountry(key, value):
    return find_latest_thing(query={key: value})


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
