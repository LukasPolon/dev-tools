""" Test module for page_search module."""
import unittest
from unittest import mock

from tools.apache_search.src import page_search

MODULE_PATH = 'tools.apache_search.src.page_search'


class TestPageSearch(unittest.TestCase):
    """ Test suite for page_search module."""

    @mock.patch(f'{MODULE_PATH}.Page')
    def test_single_page_search_files(self, mock_page):
        """ Test single_page_search_files function."""
        mock_page().files = ['file1', 'file2']
        test_url = 'https://test/url'

        result = page_search.single_page_search_files(test_url)
        self.assertEqual(result, ['file1', 'file2'])

    @mock.patch(f'{MODULE_PATH}.Page')
    def test_single_page_search_dirs(self, mock_page):
        """ Test single_page_search_dirs function."""
        mock_page().subpages = ['dir1', 'dir2']
        test_url = 'https://test/url'

        result = page_search.single_page_search_dirs(test_url)
        self.assertEqual(result, ['dir1', 'dir2'])
