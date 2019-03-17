""" Test module for apache_search module."""
import unittest

from unittest import mock
from click.testing import CliRunner

from tools.apache_search.src.cli import apache_search

MODULE_PATH = 'tools.apache_search.src.cli.apache_search'


class TestApacheSearch(unittest.TestCase):
    """ Test suite for apache_search module."""

    def setUp(self):
        """ Setup method for TestApacheSearch test suite."""
        self.runner = CliRunner()
        self.test_url = 'https://test/url'

    @mock.patch(f'{MODULE_PATH}._create_table')
    @mock.patch(f'{MODULE_PATH}.single_page_search_dirs')
    @mock.patch(f'{MODULE_PATH}.single_page_search_files')
    def test_apache_search_files(self, mock_single_files, mock_single_dirs,
                                 mock_create_table):
        """ Test apache_search command function.
            Case: display files only.
            Command: apache-search <url> --files
        """
        mock_create_table.side_effect = [
            'CREATE_TABLE_FILES',
        ]

        result = self.runner.invoke(
            apache_search.apache_search,
            ['--files', self.test_url]
        )
        self.assertEqual(result.exit_code, 0)

        exp_output = [
            f'>>>> Displaying content of: {self.test_url}',
            '>>>> FILES',
            'CREATE_TABLE_FILES'
        ]
        for output_el in exp_output:
            self.assertTrue(output_el in result.output)

        self.assertTrue(mock_single_files.called)
        self.assertTrue(mock_single_dirs.called)

    @mock.patch(f'{MODULE_PATH}._create_table')
    @mock.patch(f'{MODULE_PATH}.single_page_search_dirs')
    @mock.patch(f'{MODULE_PATH}.single_page_search_files')
    def test_apache_search_dirs(self, mock_single_files, mock_single_dirs,
                                mock_create_table):
        """ Test apache_search command function.
            Case: display dirs only.
            Command: apache-search <url> --dirs
        """
        mock_create_table.side_effect = [
            'CREATE_TABLE_DIRS',
        ]

        result = self.runner.invoke(
            apache_search.apache_search,
            ['--dirs', self.test_url]
        )
        self.assertEqual(result.exit_code, 0)

        exp_output = [
            f'>>>> Displaying content of: {self.test_url}',
            '>>>> DIRECTORIES',
            'CREATE_TABLE_DIRS'
        ]
        for output_el in exp_output:
            self.assertTrue(output_el in result.output)

        self.assertTrue(mock_single_files.called)
        self.assertTrue(mock_single_dirs.called)

    @mock.patch(f'{MODULE_PATH}._create_table')
    @mock.patch(f'{MODULE_PATH}.single_page_search_dirs')
    @mock.patch(f'{MODULE_PATH}.single_page_search_files')
    def test_apache_search_files_dirs(self, mock_single_files, mock_single_dirs,
                                      mock_create_table):
        """ Test apache_search command function.
            Case: display files and dirs.
            Command: apache-search <url>
        """
        mock_create_table.side_effect = [
            'CREATE_TABLE_FILES',
            'CREATE_TABLE_DIRS'
        ]

        result = self.runner.invoke(
            apache_search.apache_search,
            [self.test_url]
        )
        self.assertEqual(result.exit_code, 0)

        exp_output = [
            f'>>>> Displaying content of: {self.test_url}',
            '>>>> FILES',
            'CREATE_TABLE_FILES',
            '>>>> DIRECTORIES',
            'CREATE_TABLE_DIRS'
        ]
        for output_el in exp_output:
            self.assertTrue(output_el in result.output)

        self.assertTrue(mock_single_files.called)
        self.assertTrue(mock_single_dirs.called)

    @mock.patch(f'{MODULE_PATH}._create_table')
    @mock.patch(f'{MODULE_PATH}.single_page_search_dirs')
    @mock.patch(f'{MODULE_PATH}.single_page_search_files')
    def test_apache_search_urls(self, mock_single_files, mock_single_dirs,
                                mock_create_table):
        """ Test apache_search command function.
            Case: display files and dirs as urls.
            Command: apache-search <url> --display-url
        """
        mock_create_table.side_effect = [
            'CREATE_TABLE_FILES',
            'CREATE_TABLE_DIRS'
        ]

        result = self.runner.invoke(
            apache_search.apache_search,
            [self.test_url, '--display-url']
        )
        self.assertEqual(result.exit_code, 0)

        exp_output = [
            f'>>>> Displaying content of: {self.test_url}',
            '>>>> FILES',
            'CREATE_TABLE_FILES',
            '>>>> DIRECTORIES',
            'CREATE_TABLE_DIRS'
        ]
        for output_el in exp_output:
            self.assertTrue(output_el in result.output)

        self.assertTrue(mock_single_files.called)
        self.assertTrue(mock_single_dirs.called)

    @mock.patch(f'{MODULE_PATH}._create_table')
    @mock.patch(f'{MODULE_PATH}.single_page_search_dirs')
    @mock.patch(f'{MODULE_PATH}.single_page_search_files')
    def test_apache_search_negative(self, mock_single_files, mock_single_dirs,
                                    mock_create_table):
        """ Test apache_search command function.
            Case: ClickException due to both --files and --dirs options.
            Command: apache-search <url> --files --dirs
        """
        result = self.runner.invoke(
            apache_search.apache_search,
            [self.test_url, '--files', '--dirs']
        )

        exp_output = [
            f'>>>> Displaying content of: {self.test_url}',
            'Error: Options: --files and --dirs can not be used together.'
        ]

        for output_el in exp_output:
            self.assertTrue(output_el in result.output)

        self.assertNotEqual(result.exit_code, 0)
        self.assertFalse(mock_single_files.called)
        self.assertFalse(mock_single_dirs.called)
        self.assertFalse(mock_create_table.called)

    @mock.patch(f'{MODULE_PATH}.tabulate')
    def test_create_table(self, mock_tabulate):
        """ Test _create_table function."""
        test_data_list = [
            {'name': 'testfilename.txt', 'size': '200'},
            {'name': 'testfilename2.txt'}
        ]
        test_headers = ['Name', 'Size']

        apache_search._create_table(test_data_list, test_headers)
        exp_result = [['testfilename.txt', '200'], ['testfilename2.txt', None]]

        mock_tabulate.assert_called_with(
            exp_result, headers=test_headers
        )
