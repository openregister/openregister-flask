import json
import yaml

from flask import (
    current_app,
    request,
    make_response,
    render_template
)

from application import mongo
from application.repository import Repository

repository = Repository(mongo)

from flask.views import MethodView

def output_json(data, code, headers={'content-type':'application/json'}):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

def output_yaml(data, code, headers={'content-type':'text/yaml'}):
    yml = yaml.safe_dump(data)
    resp = make_response(yml, code)
    resp.headers.extend(headers or {})
    return resp

def output_html(data, code, headers={'content-type':'text/html'}, template=None):
    return render_template(template, data=data)

output_functions = {'yaml': output_yaml, 'json': output_json, 'html': output_html}

class TypeListView(MethodView):

    def get(self, extension):
        base_url = current_app.config['BASE_URL']
        types = repository.find_types()
        for type in types:
            type["url"] = "/things/%s.%s" % (type['type'], extension)

        if extension == 'html':
            return output_functions[extension](types, 200, template="types.html")
        else:
            return output_functions[extension](types, 200)

class ThingListView(MethodView):

    def get(self, type, extension):
        page = int(request.args.get('page', 1))
        page_size = current_app.config['PAGE_SIZE']
        things = repository.find_things_by_type(type, page, page_size)

        if extension == 'html':
            return output_functions[extension](things[type], 200, template="things.html")
        else:
            return output_functions[extension](things, 200)


class ThingView(MethodView):

    def get(self, type, _id, extension):
        thing = repository.find_thing_by_id(type, _id)
        if extension == 'html':
            return output_functions[extension](thing.to_primitive(), 200, template="thing.html")
        else:
            return output_functions[extension](thing.to_primitive(), 200)

