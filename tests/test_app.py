import application


app = application.app.test_client()
db = application.db
registry_url = 'http://thingstance.org/'
field_url = 'http://testing.thingstance.org/'


def test_get_unknown_domain_404():
    response = app.get('/', base_url='http://no-such-domain.example.org')
    assert response.status_code == 404


def test_get_things():
    collections = db.collection_names()
    if 'testing' not in collections:
        db.create_collection('testing')
    response = app.get('/', base_url=field_url)
    assert response.status_code == 200


def test_get_thing_404():
    hash = "aaaaaaaaa"
    response = app.get('/hash/%s' % hash, base_url=field_url)
    assert response.status_code == 404
