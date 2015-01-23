import application


app = application.app.test_client()
base_url = 'http://education.thingstance.org/'


def test_get_missing_thing_404():
    hash = "aaaaaaaaa"
    response = app.get('/Thing/%s' % hash, base_url=base_url)
    assert response.status_code == 404
