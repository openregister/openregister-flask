import application


app = application.app.test_client()
registry_url = 'http://thingstance.org/'
field_url = 'http://field.thingstance.org/'


def test_get_unknown_domain_404():
    response = app.get('/', base_url='http://no-such-domain.example.org')
    assert response.status_code == 404


def test_get_things():
    response = app.get('/', base_url=field_url)
    assert response.status_code == 200


def test_get_thing_404():
    hash = "aaaaaaaaa"
    response = app.get('/hash/%s' % hash, base_url=field_url)
    assert response.status_code == 404
