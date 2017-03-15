import application
import json

from application.registry import Register

from entry import Entry

app = application.app.test_client()
db = application.db
register = Register('testing', application.app.config['MONGO_URI'])

registry_url = 'http://openregister.org/'
field_url = 'http://testing.openregister.org/'


def setup():
    collections = db.collection_names()
    if 'testing' not in collections:
        db.create_collection('testing')

    entry = Entry()
    entry.primitive = {"id": 123, "someField": "thevalue"}
    register.put(entry)

    entry.primitive = {"id": 678, "someField": "thevalue"}
    register.put(entry)

    entry.primitive = {"id": 234, "otherField": "another value"}
    register.put(entry)


def teardown():
    db.drop_collection('testing')


def test_get_unknown_domain_404():
    response = app.get('/', base_url='http://no-such-domain.example.org')
    assert response.status_code == 404


def test_get_entries():
    response = app.get('/', base_url=field_url)
    assert response.status_code == 200


def test_get_entry_404():
    hash = "aaaaaaaaa"
    response = app.get('/hash/%s' % hash, base_url=field_url)
    assert response.status_code == 404


def test_get_entry_json_by_hash():
    entry = Entry()
    entry.primitive = {"id": 123, "someField": "thevalue"}

    response = app.get('/hash/%s.json' % entry.hash, base_url=field_url)
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert data == {"hash": entry.hash, "entry": entry.primitive}


def test_get_entry_yaml_by_hash():
    entry = Entry()
    entry.primitive = {'field': 'value'}
    register.put(entry)

    response = app.get('/hash/%s.yaml' % entry.hash, base_url=field_url)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert data == "field: value\n"


def test_search_json():
    response = app.get('/search.json?someField=thevalue',
                       base_url=field_url)
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data) == 2
    for res in data:
        assert res['hash']  # just assert there is a hash for now
        assert res['entry']['someField'] == 'thevalue'


def test_search_allows_partial_match_json():

    search_url = '/search.json?otherField=value'
    response = app.get(search_url, base_url=field_url)

    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data) == 1
    assert data[0]['hash']  # just assert there is a hash for now
    assert data[0]["entry"] == {'id': 234, 'otherField': 'another value'}


def test_search_allows_case_insensitive_match():

    search_url = '/search.json?otherField=VALUE'

    response = app.get(search_url, base_url=field_url)
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data) == 1
    assert data[0]['hash']  # just assert there is a hash for now
    assert data[0]["entry"] == {'id': 234, 'otherField': 'another value'}


def test_search_yaml():
    response = app.get('/search.yaml?otherField=another value',
                       base_url=field_url)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert data == "[id: 234\notherField: another value\n]"
