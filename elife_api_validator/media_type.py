import re

from elife_api_validator.exceptions import MissingContentType


class MediaType(object):
    params = {}
    type = ''

    def __init__(self, media_type: str) -> None:
        self._media_type = media_type
        if self._media_type:
            self._parse_content_type(self._media_type)
        else:
            raise MissingContentType('Please supply a content type')

    def _parse_content_type(self, content_type: str) -> None:
        """Parse content type string and assign type value and
        and parameter values.

        :param content_type: str
        :rtype: None
        """
        data = content_type.split(';')
        self.type = data[0]
        if len(data) > 1:
            self.params = self._unpack_params(''.join(data[1:]))

    def matches_type(self, pattern: str) -> bool:
        """Accepts a regex pattern and attempts to find a match
        with self._content_type.

        :param pattern: str
        :rtype: bool
        """
        _pattern = re.compile(pattern)
        result = _pattern.match(self._media_type)
        if result and result.group():
            return True
        return False

    @staticmethod
    def _unpack_params(params_str: str) -> dict:
        """Take formatted string and convert to param dict.

        >>> params = MediaType._unpack_params('version=1; charset=utf-8')
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
        return '{0}({1!r})'.format(self.__class__.__name__, self._media_type)

    def __str__(self) -> str:
        return self._media_type
