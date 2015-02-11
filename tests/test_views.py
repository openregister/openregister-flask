from application import views


def test_representations():
    assert 'json' in views.representations
    assert 'primitive' not in views.representations
    assert 'native' not in views.representations
    assert views.representations['json'].content_type == 'application/json'
    assert views.representations['yaml'].content_type == 'application/yaml'
