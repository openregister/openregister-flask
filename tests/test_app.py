import application


app = application.app.test_client()
registry_url = 'http://thingstance.org/'
education_url = 'http://education.thingstance.org/'


def test_get_unknown_domain_404():
    response = app.get('/', base_url='http://no-such-domain.example.org')
    assert response.status_code == 404


def test_get_tag_404():
    tag = "ThisDoesNotExist"
    response = app.get('/%s' % tag, base_url=education_url)
    assert response.status_code == 404


def test_get_thing_404():
    hash = "aaaaaaaaa"
    response = app.get('/Thing/%s' % hash, base_url=education_url)
    assert response.status_code == 404
