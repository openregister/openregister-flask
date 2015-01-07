import json

from flask import render_template, request, current_app
from application import app
from .resources import TypeListView, ThingListView, ThingView, output_json
from application.resources import repository
from thingstance import Thing


app.add_url_rule('/things.<string:extension>', view_func=TypeListView.as_view('type_list'))

app.add_url_rule('/things/<string:type>.<string:extension>', view_func=ThingListView.as_view('thing_list'))

app.add_url_rule('/things/<string:type>/<string:_id>.<string:extension>', view_func=ThingView.as_view('type_view'))

@app.route("/")
def index():
    return render_template("index.html", base_url=app.config['BASE_URL'])

@app.route("/things", methods=['POST'])
def things():
    thing = Thing(request.json)
    uid = repository.save_thing(thing)
    return output_json({'uid' : str(uid)}, 200)

@app.route("/things/<string:type>")
def thing_for_user(type):
    things = repository.find_thing_by_owner(type, request.args.get('issuedFor'))
    return output_json(things, 200)

