from elife_api_validator.media_type import MediaType


def test_it_can_return_correct_repr():
    content_type = 'application/vnd.elife.article-list+json'
    media_type = MediaType(content_type)
    assert repr(media_type) == "MediaType({!r})".format(content_type)


def test_it_can_match_type():
    content_type = 'application/vnd.elife.article-list+json; version=1'
    media_type = MediaType(content_type)
    assert media_type.matches_type('application\/([a-z-\.]*\+)json') is True


def test_it_will_fail_to_match_invalid_type():
    content_type = 'application/some_invalid_type+something; version=1'
    media_type = MediaType(content_type)
    assert media_type.matches_type('application\/([a-z-\.]*\+)json') is False


def test_it_can_unpack_single_param():
    params = 'version=1'
    assert MediaType.unpack_params(params) == {'version': '1'}


def test_it_can_unpack_mulitple_params():
    params = 'version=1; charset=utf-8'
    assert MediaType.unpack_params(params) == {'version': '1', 'charset': 'utf-8'}


def test_it_can_parse_content_type_on_init():
    content_type = 'application/vnd.elife.article-list+json; version=1'
    media_type = MediaType(content_type)
    assert media_type.type == 'application/vnd.elife.article-list+json'
    assert len(media_type.params) == 1


def test_it_can_get_type_str():
    content_type = 'application/vnd.elife.article-list+json; version=1'
    media_type = MediaType(content_type)
    assert media_type.get_type_str() == 'article-list.v1'


def test_it_can_get_content_type():
    content_type = 'application/vnd.elife.article-list+json; version=1'
    media_type = MediaType(content_type)
    assert media_type.content_type == content_type


def test_it_will_provide_a_default_version_if_not_present():
    content_type = 'application/vnd.elife.article-list+json'
    media_type = MediaType(content_type)
    assert media_type.get_type_str() == 'article-list.v1'
