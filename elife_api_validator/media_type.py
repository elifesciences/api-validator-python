import re

from elife_api_validator.exceptions import MissingContentType


class MediaType(object):
    params = {}
    type = ''

    def __init__(self, content_type: str) -> None:
        """
        >>> mt = MediaType(content_type='application/vnd.elife.article-list+json; version=1')

        :param content_type: str
        """

        self._content_type = content_type
        if self._content_type:
            self.parse_content_type(self._content_type)
        else:
            raise MissingContentType('Please supply a content type')

    @property
    def content_type(self):
        return self._content_type

    def get_type_str(self) -> str:
        """Returns a formatted content type string.

        >>> media_type = MediaType('application/vnd.elife.article-list+json; version=1')
        >>> print(media_type.get_type_str())
        'article-list.v1'

        :rtype: str
        """
        # CHANGE TO REGEX SEARCH !!
        type_str = self.type.split('.')[-1].replace('application/', '').replace('+json', '')

        return '{type}.v{version}'.format(type=type_str,
                                          version=self.params.get('version', '1'))

    def parse_content_type(self, content_type: str) -> None:
        """Parse content type string and assign type value and
        and parameter values.


        :param content_type: str
        :rtype: None
        """
        data = content_type.split(';')
        self.type = data[0]
        if len(data) > 1:
            self.params = self.unpack_params(data[1])

    def matches_type(self, pattern: str) -> bool:
        """Accepts a regex pattern and attempts to find a match
        with self._content_type.

        :param pattern: str
        :rtype: bool
        """
        _pattern = re.compile(pattern)
        result = _pattern.match(self._content_type)
        if result and result.group():
            return True
        return False

    @staticmethod
    def unpack_params(params_str: str) -> dict:
        """Take formatted string and convert to param dict.

        >>> params = MediaType.unpack_params('version=1; charset=utf-8')
        >>> params
        {'version': '1', 'charset: 'utf-8'}

        :param params_str: str
        :rtype: dict
        """
        params = {}

        for param in params_str.replace(';', '').split():
            param_list = param.split('=')
            params[param_list[0]] = param_list[1]

        return params

    def __repr__(self) -> str:
        return '{0}({1!r})'.format(self.__class__.__name__, self._content_type)
