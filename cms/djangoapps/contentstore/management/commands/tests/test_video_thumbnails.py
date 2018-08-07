# -*- coding: utf-8 -*-
"""
Tests for course video thumbnails management command.
"""

from mock import patch
from django.test import TestCase
from django.core.management import call_command, CommandError
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

LOGGER_NAME = "cms.djangoapps.contentstore.tasks"


class TestArgParsing(TestCase):
    """
    Tests for parsing arguments for the `migrate_transcripts` management command
    """
    def test_no_args(self):
        errstring = "Must specify --from_settings"
        with self.assertRaisesRegexp(CommandError, errstring):
            call_command('migrate_transcripts')



class TestVideoThumbnails(ModuleStoreTestCase):
    """
    Tests adding thumbnails to course videos from YouTube
    """
    def setUp(self):
        """ Common setup. """
        super(TestVideoThumbnails, self).setUp()

    def test_video_thumbnails_call_count_with_commit(self, mocked_api):
        """
        Test updating thumbnails with commit
        """
        course_videos = [
            ('test-course1', 'super-soaker', 'https://www.youtube.com/watch?v=OscRe3pSP80'),
            ('test-course2', 'medium-soaker', 'https://www.youtube.com/watch?v=OscRe3pSP81')
        ]
        with patch('edxval.api.get_course_video_ids_with_youtube_profile', return_value=course_videos):
            with patch('_latest_settings') as settings:
                with patch('cms.djangoapps.contentstore.tasks.enqueue_update_thumbnail_tasks') as tasks:
                    settings.all_course_videos = True
                    settings.commit = True
                    settings.batch_size = 10
                    call_command('video_thumbnails', '--from-settings')
                    self.assertEquals(tasks.called, True, msg='method should be called')
                    self.assertEquals(tasks.call_count, 1)
