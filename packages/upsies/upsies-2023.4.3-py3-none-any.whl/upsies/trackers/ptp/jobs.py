"""
Concrete :class:`~.base.TrackerJobsBase` subclass for PTP
"""

import functools
from datetime import datetime

from ... import errors, jobs, utils
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase
from ._ptp_tags import PTP_TAGS

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PtpTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Common background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,
            self.ptp_group_id_job,
            self.description_job,

            # Common interactive jobs
            self.type_job,
            self.imdb_job,
            self.scene_check_job,

            # Interactive jobs that only run if movie does not exists on PTP yet
            self.title_job,
            self.year_job,
            self.plot_job,
            self.tags_job,
            self.cover_art_job,
        )

    @functools.cached_property
    def type_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('type'),
            label='Type',
            precondition=self.make_precondition('type_job'),
            autodetect=self.autodetect_type,
            choices=(
                ('Feature Film', 'Feature Film'),
                ('Short Film', 'Short Film'),
                ('Miniseries', 'Miniseries'),
                ('Stand-up Comedy', 'Stand-up Comedy'),
                ('Live Performance', 'Live Performance'),
                ('Movie Collection', 'Movie Collection'),
            ),
            callbacks={
                'finished': self.update_imdb_query,
            },
            **self.common_job_args(),
        )

    def autodetect_type(self, _):
        if self.release_name.type == ReleaseType.season:
            return 'Miniseries'

        # Short film if runtime 45 min or less (Rule 1.1.1)
        # NOTE: This doesn't work for VIDEO_TS releases. We could sum the
        #       duration of all .VOB files, but they notoriously lie about their
        #       duration. For now, the user can always correct the autodetected
        #       type.
        main_video = utils.video.filter_main_videos(
            tuple(utils.video.find_videos(self.content_path))
        )[0]
        if utils.video.duration(main_video) <= 45 * 60:
            return 'Short Film'

    def update_imdb_query(self, type_job_):
        """
        Set :attr:`~.webdbs.common.Query.type` on
        :attr:`~.TrackerJobsBase.imdb_job` to :attr:`~.ReleaseType.movie` or
        :attr:`~.ReleaseType.series` depending on the output of :attr:`type_job`
        """
        assert self.type_job.is_finished
        if self.type_job.output:
            new_type = self.type_job.output[0]
            if new_type == 'Feature Film':
                _log.debug('Updating IMDb query type: %r', utils.release.ReleaseType.movie)
                self.imdb_job.query.type = utils.release.ReleaseType.movie
            elif new_type == 'Miniseries':
                _log.debug('Updating IMDb query type: %r', utils.release.ReleaseType.series)
                self.imdb_job.query.type = utils.release.ReleaseType.series

    @functools.cached_property
    def description_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            prejobs=(
                self.mediainfo_job,
                self.upload_screenshots_job,
            ),
            text=self.generate_description,
            autofinish=True,
            read_only=True,
            hidden=True,
            precondition=self.make_precondition('description_job'),
            **self.common_job_args(ignore_cache=True),
        )

    async def generate_description(self):
        original_release_name = (
            '[size=4]'
            + '[b]'
            + utils.fs.basename(
                utils.fs.strip_extension(self.content_path)
            )
            + '[/b]'
            + '[/size]'
        )

        # Join mediainfos + screenshots for each movie/episode into
        # sections. Each section may contain multiple mediainfos (.IFO/.VOB).
        tags = []
        subtags = []
        for video_path, info in self.mediainfos_and_screenshots.items():
            if info['mediainfo']:
                subtags.append(f'[mediainfo]{info["mediainfo"]}[/mediainfo]')
            if info['screenshot_urls']:
                subtags.append('\n'.join(
                    f'[img={url}]'
                    for url in info['screenshot_urls']
                ))
                tags.append(''.join(subtags))
                subtags.clear()

        description = (
            original_release_name
            + '\n\n'
            + '\n[hr]\n'.join(tags)
        )
        return description

    mediainfo_from_all_videos = True
    screenshots_from_all_videos = True

    @functools.cached_property
    def screenshots_count(self):
        """
        How many screenshots to make

        Use :attr:`options`\\ ``["screenshots"]`` it it exists. This value
        should be explicitly set by the user, e.g. via a CLI argument or GUI
        element.

        Use :attr:`options`\\ ``["screenshots_from_movie"]`` for uploads that
        contain a single video file.

        Use :attr:`options`\\ ``["screenshots_from_episode"]`` for uploads that
        contain multiple video files.
        """
        # CLI option, GUI widget, etc
        if self.options.get('screenshots'):
            return self.options['screenshots']

        # Get that same video files that were passed to ScreenshotsJob in
        # JobBase.screenshots_job.
        video_files = utils.torrent.filter_files(
            self.content_path,
            exclude=self.exclude_files,
        )
        # Exclude samples, extras, DVD menus, etc
        video_files = utils.video.filter_main_videos(video_files)
        if len(video_files) == 1:
            return self.options['screenshots_from_movie']
        else:
            return self.options['screenshots_from_episode']

    @property
    def imdb_id(self):
        if self.imdb_job.is_finished:
            return self.imdb_job.output[0]

    @functools.cached_property
    def ptp_group_id_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('ptp-group-id'),
            label='PTP Group ID',
            precondition=self.make_precondition('ptp_group_id_job'),
            prejobs=(
                self.imdb_job,
            ),
            worker=self.fetch_ptp_group_id,
            catch=(errors.RequestError,),
            **self.common_job_args(),
        )

    async def fetch_ptp_group_id(self, _):
        assert self.imdb_job.is_finished
        group_id = await self.tracker.get_ptp_group_id_by_imdb_id(self.imdb_id)
        return '' if group_id is None else group_id

    @property
    def ptp_group_id(self):
        """
        PTP group ID if :attr:`ptp_group_id_job` is finished and group ID
        was found, `None` otherwise
        """
        if self.ptp_group_id_job.is_finished:
            if self.ptp_group_id_job.output:
                return self.ptp_group_id_job.output[0]

    def ptp_group_does_not_exist(self):
        """
        Whether the server already has a group for :attr:`imdb_id`

        :attr:`ptp_group_id_job` must be finished when this is called.

        This is used as a :attr:`~.JobBase.precondition` for jobs that are only
        needed if the server doesn't have any releases for this :attr:`imdb_id`
        yet.
        """
        assert self.ptp_group_id_job.is_finished
        if self.ptp_group_id:
            return False
        else:
            return True

    @functools.cached_property
    def title_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('title'),
            label='Title',
            precondition=self.make_precondition(
                'title_job',
                precondition=self.ptp_group_does_not_exist,
            ),
            prejobs=(
                self.ptp_group_id_job,
                self.imdb_job,
            ),
            text=self.fetch_title,
            normalizer=self.normalize_title,
            validator=self.validate_title,
            **self.common_job_args(),
        )

    async def fetch_title(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='title')

    def normalize_title(self, text):
        return text.strip()

    def validate_title(self, text):
        if not text:
            raise ValueError('Title must not be empty')

    @functools.cached_property
    def year_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('year'),
            label='Year',
            precondition=self.make_precondition(
                'year_job',
                precondition=self.ptp_group_does_not_exist,
            ),
            prejobs=(
                self.ptp_group_id_job,
                self.imdb_job,
            ),
            text=self.fetch_year,
            normalizer=self.normalize_year,
            validator=self.validate_year,
            **self.common_job_args(),
        )

    async def fetch_year(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='year')

    def normalize_year(self, text):
        return text.strip()

    def validate_year(self, text):
        try:
            year = int(text)
        except ValueError:
            raise ValueError('Year is not a number')
        else:
            if not 1800 < year < datetime.now().year + 10:
                raise ValueError('Year is not reasonable')

    @functools.cached_property
    def tags_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('tags'),
            label='Tags',
            precondition=self.make_precondition(
                'tags_job',
                precondition=self.ptp_group_does_not_exist,
            ),
            prejobs=(
                self.ptp_group_id_job,
                self.imdb_job,
            ),
            text=self.fetch_tags,
            normalizer=self.normalize_tags,
            validator=self.validate_tags,
            **self.common_job_args(),
        )

    async def fetch_tags(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='tags')

    def normalize_tags(self, text):
        tags = [tag.strip() for tag in text.split(',')]
        deduped = list(dict.fromkeys(tags))
        return ', '.join(tag for tag in deduped if tag)

    def validate_tags(self, text):
        for tag in text.split(','):
            tag = tag.strip()
            if tag and tag not in PTP_TAGS:
                raise ValueError(f'Tag is not valid: {tag}')

    @functools.cached_property
    def cover_art_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('cover_art'),
            label='Cover Art',
            precondition=self.make_precondition(
                'cover_art_job',
                precondition=self.ptp_group_does_not_exist,
            ),
            prejobs=(
                self.ptp_group_id_job,
                self.imdb_job,
            ),
            text=self.fetch_cover_art,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_cover_art(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='art')

    @functools.cached_property
    def plot_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('plot'),
            label='Plot',
            precondition=self.make_precondition(
                'plot_job',
                precondition=self.ptp_group_does_not_exist,
            ),
            prejobs=(
                self.ptp_group_id_job,
                self.imdb_job,
            ),
            text=self.fetch_plot,
            normalizer=self.normalize_plot,
            validator=self.validate_plot,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_plot(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='plot')

    def normalize_plot(self, text):
        return text.strip()

    def validate_plot(self, text):
        if not text:
            raise ValueError('Plot must not be empty')

    @property
    def post_data(self):
        post_data = self._post_data_common

        _log.debug('PTP group ID: %r', self.ptp_group_id)
        if self.ptp_group_id:
            _log.debug('Adding format to existing group')
            post_data.update(self._post_data_add_format)
        else:
            _log.debug('Creating new group')
            post_data.update(self._post_data_add_movie)

        return post_data

    @property
    def _post_data_common(self):
        data = {
            # Feature Film, Miniseries, Short Film, etc
            'type': self.get_job_attribute(self.type_job, 'choice'),

            # Mediainfo and Screenshots
            'release_desc': self.get_job_output(self.description_job, slice=0),

            # Value that are autodetected server-side
            # 'source': 'Other',  # Custom source
            # 'other_source': ...,
            # 'codec': 'Other',  # Custom codec
            # 'other_codec': ...,
            # 'resolution': ...,  # 1080p, 720p, etc
            # 'other_resolution': ...,  # Custom resolution, e.g. 423x859
            # 'container': 'Other',  # Custom container
            # 'other_container': ...,
            # 'subtitles[]': releaseInfo.Subtitles,
            # 'trumpable[]': releaseInfo.Trumpable,

            # TODO

            # 'remaster_title': ...,  # Edition Information ("Director's Cut", "Dual Audio", etc.)
            # 'remaster_year': ...,
            # 'remaster_other_input': ...,

            # Is not main movie (bool)
            'special': '1' if self.options['not_main_movie'] else None,

            # Is personal rip (bool)
            'internalrip': '1' if self.options['personal_rip'] else None,

            # Is scene Release (bool)
            'scene': '1' if self.get_job_attribute(self.scene_check_job, 'is_scene_release') else None,

            # .nfo file content
            'nfo_text': self.read_nfo(),

            # Upload token from staff
            'uploadtoken': self.options.get('upload_token', None),
        }

        # Tick "Edition Information" checkbox?
        if any(data.get(key, False) for key in (
                'remaster_year',
                'remaster_title',
                'remaster_other_input',
        )):
            data['remaster'] = '1'

        return data

    @property
    def _post_data_add_format(self):
        # Upload release to movie that exists on PTP
        return {
            'groupid': self.ptp_group_id,
        }

    @property
    def _post_data_add_movie(self):
        # Upload movie that is not on PTP yet in any format
        post_data = {
            # IMDb ID (must be 7 characters without the leading "tt")
            'imdb': self.tracker.normalize_imdb_id(self.imdb_id),
            # Release year
            'title': self.get_job_output(self.title_job, slice=0),
            # Release year
            'year': self.get_job_output(self.year_job, slice=0),
            # Movie plot or summary
            'album_desc': self.get_job_output(self.plot_job, slice=0),
            # Genre
            'tags': self.get_job_output(self.tags_job, slice=0),
            # Youtube ID
            # 'trailer': ...,
            # Poster URL
            'image': self.get_job_output(self.cover_art_job, slice=0),
        }

        # TODO: Send artists
        # # ???: For some reason PtpUploader uses "artist" and "importance" in the
        # #      POST data while the website form uses "artists", "importances"
        # #      and "roles".
        # artists = self.get_job_output(self.artists_job):
        # if artists:
        #     post_data['artist'] = []
        #     post_data['importance'] = []
        #     for name in artists:
        #         # `importance` is the artist type:
        #         # 1: Director
        #         # 2: Writer
        #         # 3: Producer
        #         # 4: Composer
        #         # 5: Actor
        #         # 6: Cinematographer
        #         post_data['importance'].append('1')
        #         post_data['artist'].append(name)
        #         post_data['role'].append(name)

        return post_data

    def read_nfo(self):
        try:
            return utils.string.read_nfo(self.content_path)
        except errors.ContentError as e:
            self.error(e)

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
