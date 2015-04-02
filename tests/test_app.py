import application

app = application.app.test_client()
db = application.db
registry_url = 'http://openregister.org/'
field_url = 'http://testing.openregister.org/'


def test_get_unknown_domain_404():
    response = app.get('/', base_url='http://no-such-domain.example.org')
    assert response.status_code == 404


def test_get_entries():
    collections = db.collection_names()
    if 'testing' not in collections:
        db.create_collection('testing')
    response = app.get('/', base_url=field_url)
    assert response.status_code == 200


def test_get_entry_404():
    hash = "aaaaaaaaa"
    response = app.get('/hash/%s' % hash, base_url=field_url)
    assert response.status_code == 404


def test_search():
    collections = db.collection_names()
    if 'testing' not in collections:
        db.create_collection('testing')
    collection = db['testing']
    collection.remove()
    collection.insert({"id": 123, "someField": "thevalue"})
    collection.insert({"id": 678, "someField": "thevalue"})
    collection.insert({"id": 234, "someField": "another value"})

    response = app.get('/search.json?field=someField&value=thevalue',
                       base_url=field_url)
    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert body == '[{"id":123,"someField":"thevalue"},' \
                   '{"id":678,"someField":"thevalue"}]'
