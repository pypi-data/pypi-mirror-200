"""
Concrete :class:`~.base.TrackerBase` subclass for PTP
"""

import re
import urllib

from ... import errors, utils
from ..base import TrackerBase
from .config import PtpTrackerConfig
from .jobs import PtpTrackerJobs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PtpTracker(TrackerBase):
    name = 'ptp'
    label = 'PTP'

    setup_howto_template = (
        'TODO'
    )

    TrackerConfig = PtpTrackerConfig
    TrackerJobs = PtpTrackerJobs

    @property
    def _base_url(self):
        return self.options['base_url']

    @property
    def _ajax_url(self):
        return urllib.parse.urljoin(self._base_url, '/ajax.php')

    @property
    def _logout_url(self):
        return urllib.parse.urljoin(self._base_url, '/logout.php')

    @property
    def _upload_url(self):
        return urllib.parse.urljoin(self._base_url, '/upload.php')

    @property
    def _torrents_url(self):
        return urllib.parse.urljoin(self._base_url, '/torrents.php')

    @property
    def _announce_url(self):
        announce_url = self.options['announce_url']
        if not announce_url:
            raise errors.AnnounceUrlNotSetError(tracker=self)
        else:
            return self.options['announce_url']

    @property
    def _passkey(self):
        # Needed for logging in with ajax.php
        match = re.search(r'.*/([a-zA-Z0-9]+)/announce', self._announce_url)
        if match:
            return match.group(1)
        else:
            raise RuntimeError(f'Failed to find passkey in announce URL: {self._announce_url}')

    async def _request(self, method, *args, error_prefix='', **kwargs):
        # Because HTTP errors (e.g. 404) are raised, we treat RequestErrrors as
        # normal response so we can get the message from the HTML.
        try:
            # `method` is "GET" or "POST"
            response = await getattr(utils.http, method.lower())(
                *args,
                user_agent=True,
                follow_redirects=False,
                **kwargs,
            )
        except errors.RequestError as e:
            response = e

        # Get error from regular exception (e.g. "Connection refused") or the
        # HTML in response.
        try:
            self._maybe_raise_error(response)
        except errors.RequestError as e:
            # Prepend error_prefix to explain the general nature of the error.
            if error_prefix:
                raise errors.RequestError(f'{error_prefix}: {e}')
            else:
                raise e
        else:
            return response

    def _maybe_raise_error(self, response_or_request_error):
        # utils.http.get()/post() raise RequestError on HTTP status codes, but
        # we want to get the error message from the response text.
        # _maybe_raise_error_from_*() handle Response and RequestError.
        self._maybe_raise_error_from_json(response_or_request_error)
        self._maybe_raise_error_from_html(response_or_request_error)

        # If we got a RequestError and we didn't find an error message in the
        # text, we raise it. This handles any real RequestErrors, like
        # "Connection refused". We also raise any other exception so _request()
        # doesn't return it as a regular response.
        if isinstance(response_or_request_error, BaseException):
            raise response_or_request_error

    def _maybe_raise_error_from_json(self, response_or_request_error):
        # Get error message from ajax.php JSON Response or RequestError
        try:
            json = response_or_request_error.json()
        except errors.RequestError:
            # Response or RequestError is not JSON
            pass
        else:
            if (
                isinstance(json, dict)
                and json.get('Result') == 'Error'
                and json.get('Message')
            ):
                raise errors.RequestError(json['Message'])

    def _maybe_raise_error_from_html(self, response_or_request_error):
        # Only attempt to find an error message if this looks like HTML. This
        # prevents a warning from bs4 that tries to be helpful.
        text = str(response_or_request_error)
        if all(c in text for c in '<>\n'):
            doc = utils.html.parse(text)
            try:
                error_header_tag = doc.select('#content .page__title', string=re.compile(r'(?i:error)'))
                error_container_tag = error_header_tag[0].parent
                error_msg_tag = error_container_tag.find('div', attrs={'class': 'panel__body'})
                error_msg = error_msg_tag.get_text().strip()
                if error_msg:
                    raise errors.RequestError(error_msg)
            except (AttributeError, IndexError):
                # No error message found
                pass

    def _get_anti_csrf_token(self, response):
        json = response.json()
        return json['AntiCsrfToken']

    _auth_regex = re.compile(r'logout\.php\?.*\bauth=([0-9a-fA-F]+)')

    async def _get_auth(self):
        assert self.is_logged_in
        response = await self._request('GET', self._base_url)
        doc = utils.html.parse(response)

        try:
            logout_link_tag = doc.find('a', href=self._auth_regex)
            logout_link_href = logout_link_tag['href']
            match = self._auth_regex.search(logout_link_href)
            return match.group(1)
        except (AttributeError, KeyError, TypeError):
            pass

        raise RuntimeError('Could not find auth')

    async def _login(self):
        if not self.options.get('username'):
            raise errors.RequestError('Login failed: No username configured')
        elif not self.options.get('password'):
            raise errors.RequestError('Login failed: No password configured')

        _log.debug('%s: Logging in as %r', self.name, self.options['username'])
        post_data = {
            'username': self.options['username'],
            'password': self.options['password'],
            'passkey': self._passkey,
            # 'keeplogged': '1',
        }
        response = await self._request(
            method='POST',
            url=f'{self._ajax_url}?action=login',
            data=post_data,
            error_prefix='Login failed',
        )
        self._anti_csrf_token = self._get_anti_csrf_token(response)

    async def _logout(self):
        try:
            _log.debug('%s: Logging out', self.name)
            await self._request(
                method='GET',
                url=self._logout_url,
                params={'auth': await self._get_auth()},
                error_prefix='Logout failed',
            )

        finally:
            if hasattr(self, '_anti_csrf_token'):
                delattr(self, '_anti_csrf_token')

    async def get_announce_url(self):
        return self._announce_url

    async def upload(self, tracker_jobs):
        post_data = tracker_jobs.post_data
        post_data['AntiCsrfToken'] = self._anti_csrf_token
        _log.debug('POSTing data:')
        for k, v in post_data.items():
            _log.debug(' * %s = %s', k, v)

        post_files = {
            'file_input': {
                'file': tracker_jobs.torrent_filepath,
                'mimetype': 'application/x-bittorrent',
            },
        }
        _log.debug('POSTing files: %r', post_files)

        # response = await utils.http.post(
        #     url=self._upload_url,
        #     cache=False,
        #     user_agent=True,
        #     # Can we use this to get the page of the uploaded torrent?
        #     # follow_redirects=False,
        #     data=post_data,
        #     files=post_files,
        # )
        # utils.html.dump(response, 'ptp_upload_response.html')

        self.error('PTP support is not done yet.')

    def normalize_imdb_id(self, imdb_id):
        """
        Format IMDb ID for PTP

        PTP expects 7-characters, right-padded with "0" and without the leading
        "tt".

        If `imdb_id` is `None`, return "0".
        """
        if imdb_id is None:
            return '0'
        else:
            return str(imdb_id).lstrip('t').rjust(7, '0')

    async def get_ptp_group_id_by_imdb_id(self, imdb_id):
        """
        Convert IMDb ID to PTP group ID

        Any :class:`~.RequestError` is caught and passed to
        :meth:`.TrackerBase.error`.

        :return: PTP group ID or `None` if PTP doesn't have a group for
            `imdb_id`
        """
        _log.debug('%s: Fetching PTP group ID', imdb_id)
        try:
            await self.login()
            response = await self._request(
                method='GET',
                url=self._torrents_url,
                params={
                    'imdb': self.normalize_imdb_id(imdb_id),
                    'json': '1',
                },
                cache=True,
            )

        except errors.RequestError as e:
            self.error(e)

        else:
            match = re.search(r'id=(\d+)', response.headers.get('location', ''))
            if match:
                _log.debug('%s: PTP group ID: %s', imdb_id, match.group(1))
                return match.group(1)
            else:
                _log.debug('%s: No PTP group ID', imdb_id)

    async def get_ptp_metadata(self, imdb_id, key=None):
        """
        Get metadata from PTP website

        Any :class:`~.RequestError` is caught and passed to
        :meth:`.TrackerBase.error`.

        :param imdb_id: IMDb ID (e.g. ``tt123456``)
        """
        if key:
            _log.debug('%s: Fetching %s from PTP', imdb_id, key)
        else:
            _log.debug('%s: Fetching metadata from PTP', imdb_id, key)

        assert imdb_id, imdb_id

        try:
            await self.login()
            response = await self._request(
                method='GET',
                url=self._ajax_url,
                params={
                    'action': 'torrent_info',
                    'imdb': self.normalize_imdb_id(imdb_id),
                },
                cache=True,
            )
            # Raise RequestError if response is not valid JSON
            results = response.json()

        except errors.RequestError as e:
            self.error(e)

        else:
            assert len(results) == 1
            if key is None:
                _log.debug('%s: PTP metadata: %s', imdb_id, results[0])
                return results[0]
            else:
                _log.debug('%s: PTP %s: %s', imdb_id, key, results[0][key])
                return results[0][key]
