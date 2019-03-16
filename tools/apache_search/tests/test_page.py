""" Test module for Page class."""
import unittest
from unittest import mock

from tools.apache_search.src.page import Page


MODULE_PATH = 'tools.apache_search.src.page'


class TestPage(unittest.TestCase):
    """ Test class for Page class. """
    def setUp(self):
        """ Setup method for the Page class tests."""
        self.mock_page = mock.MagicMock(spec=Page, name='mock_page')

    def tearDown(self):
        """ Teardown method for Page class tests."""
        self.mock_page.reset_mock()

    def test_init(self):
        """ Init method test for the Page class tests."""
        custom_url = 'https://domain/dir/'
        test_page = Page(custom_url)

        self.assertEqual(test_page._url, custom_url)
        self.assertEqual(test_page._subpages, None)
        self.assertEqual(test_page._files, None)
        self.assertEqual(test_page._page_bs, None)

    @mock.patch(f'{MODULE_PATH}.Page._get_subpages')
    def test_subpages(self, mock_get_subpages):
        """ Test subpages property method.
            Variable self._subpages is None.
        """
        test_page = Page('http://custom_url')
        self.assertEqual(test_page.subpages, mock_get_subpages())

    @mock.patch(f'{MODULE_PATH}.Page._get_subpages')
    def test_subpages_not_none(self, mock_get_subpages):
        """ Test subpages property method.
            Variable self._subpages is not None.
        """
        test_page = Page('http://custom_url')
        test_page._subpages = 'custom_subpages'
        self.assertEqual(test_page.subpages, 'custom_subpages')
        self.assertFalse(mock_get_subpages.called)

    @mock.patch(f'{MODULE_PATH}.Page._get_files')
    def test_files(self, mock_get_files):
        """ Test files property method.
            Variable self._files is None.
        """
        test_page = Page('http://custom_url')
        self.assertEqual(test_page.files, mock_get_files())

    @mock.patch(f'{MODULE_PATH}.Page._get_files')
    def test_files_not_none(self, mock_get_files):
        """ Test files property method.
            Variable self._files is not None.
        """
        test_page = Page('http://custom_url')
        test_page._files = 'custom_files'
        self.assertEqual(test_page.files, 'custom_files')
        self.assertFalse(mock_get_files.called)

    @mock.patch(f'{MODULE_PATH}.requests')
    def test_get_raw_page_positive(self, mock_requests):
        """ Test _get_raw_page method.
            Case: positive, no Connection Error raised.
        """
        test_url = 'https://test/url/'
        self.mock_page._url = test_url

        exp_result = 'request_text_result'
        mock_requests_get = mock.MagicMock(name='mock_requests_get')
        mock_requests_get.text = exp_result
        mock_requests_get.status_code = 200
        mock_requests.get.return_value = mock_requests_get

        result = Page._get_raw_page(self.mock_page)

        self.assertEqual(result, exp_result)
        self.assertTrue(mock_requests.get.called)

    @mock.patch(f'{MODULE_PATH}.requests')
    def test_get_raw_page_connection_error(self, mock_requests):
        """" Test _get_raw_page method.
             Case: negative, Connection Error raised.
        """
        test_url = 'https://test/url/'
        self.mock_page._url = test_url

        mock_requests_get = mock.MagicMock(name='mock_requests_get')
        mock_requests_get.status_code = 404
        mock_requests.get.return_value = mock_requests_get

        with self.assertRaises(ConnectionError):
            Page._get_raw_page(self.mock_page)

    @mock.patch(f'{MODULE_PATH}.BeautifulSoup')
    def test_get_bs(self, mock_bs):
        """ Test _get_bs method.
            Case: variable self._page_bs is None.
        """
        self.mock_page._page_bs = None
        result = Page._get_bs(self.mock_page)

        self.assertEqual(result, mock_bs())
        self.assertTrue(self.mock_page._get_raw_page.called)

    @mock.patch(f'{MODULE_PATH}.BeautifulSoup')
    def test_get_bs_not_none(self, mock_bs):
        """ Test _get_bs method.
            Case: variable self._page_bs is not None.
        """
        self.mock_page._page_bs = 'BS'
        result = Page._get_bs(self.mock_page)

        self.assertEqual(result, 'BS')
        self.assertFalse(mock_bs.called)
        self.assertFalse(self.mock_page._get_raw_page.called)

    def test_get_files(self):
        """ Test _get_files method."""
        mock_bs = mock.MagicMock(name='mock_bs')
        mock_table_element = mock.MagicMock(name='mock_table_element')
        mock_table_element.find_all.return_value = 'table_el_find_all'
        mock_bs.find_all.return_value = [mock_table_element]
        self.mock_page._get_bs.return_value = mock_bs
        self.mock_page._find_alt_elements.return_value = [True]
        self.mock_page._parse_td_text_vals.return_value = 'file_value'

        result = Page._get_files(self.mock_page)
        self.assertEqual(result, ['file_value'])

    def test_get_subpages(self):
        """ Test _get_subpages method."""
        mock_bs = mock.MagicMock(name='mock_bs')
        mock_table_element = mock.MagicMock(name='mock_table_element')
        mock_table_element.find_all.return_value = 'table_el_find_all'
        mock_bs.find_all.return_value = [mock_table_element]
        self.mock_page._get_bs.return_value = mock_bs
        self.mock_page._find_alt_elements.return_value = [True]
        self.mock_page._parse_td_text_vals.return_value = 'subpage_value'

        result = Page._get_subpages(self.mock_page)
        self.assertEqual(result, ['subpage_value'])

    @mock.patch(f'{MODULE_PATH}.re.compile')
    def test_find_alt_elements_files(self, mock_compile):
        """ Test _find_alt_elements method.
            Case: target - files.
        """
        target = 'files'

        alt_element_ico = mock.MagicMock(name='alt_ico')
        alt_element_ico.attrs = {'alt': '[ICO]'}
        alt_element_ico.find.return_value = alt_element_ico

        alt_element_parentdir = mock.MagicMock(name='alt_parentdir')
        alt_element_parentdir.attrs = {'alt': '[PARENTDIR]'}
        alt_element_parentdir.find.return_value = alt_element_parentdir

        alt_element_dir = mock.MagicMock(name='alt_dir')
        alt_element_dir.attrs = {'alt': '[DIR]'}
        alt_element_dir.find.return_value = alt_element_dir

        alt_element_blank = mock.MagicMock(name='alt_blank')
        alt_element_blank.attrs = {'alt': '[   ]'}
        alt_element_blank.find.return_value = alt_element_blank

        td_elements = [
            alt_element_ico,
            alt_element_parentdir,
            alt_element_dir,
            alt_element_blank
        ]

        result = Page._find_alt_elements(self.mock_page, target, td_elements)
        self.assertEqual(result, [alt_element_blank])
        self.assertTrue(mock_compile.called)

    @mock.patch(f'{MODULE_PATH}.re.compile')
    def test_find_alt_elements_dirs(self, mock_compile):
        """ Test _find_alt_elements method.
            Case: target - dirs.
        """
        target = 'dirs'

        alt_element_dir = mock.MagicMock(name='alt_dir')
        alt_element_dir.attrs = {'alt': '[DIR]'}
        alt_element_dir.find.return_value = alt_element_dir

        alt_element_blank = mock.MagicMock(name='alt_blank')
        alt_element_blank.attrs = {'alt': '[   ]'}
        alt_element_blank.find.return_value = alt_element_blank

        td_elements = [
            alt_element_blank,
            alt_element_dir
        ]

        result = Page._find_alt_elements(self.mock_page, target, td_elements)
        self.assertEqual(result, [alt_element_dir])
        self.assertTrue(mock_compile.called)

    @mock.patch(f'{MODULE_PATH}.datetime')
    def test_parse_td_text_vals_file(self, mock_datetime):
        """ Test _parse_td_text_vals method.
            Case: file element.

            No test isolation for testing regex compilations.
        """
        text_val_name = mock.MagicMock(name='text_name')
        text_val_name.text = 'testfilename.extension'

        text_val_datetime = mock.MagicMock(name='text_datetime')
        text_val_datetime.text = '2019-03-16 11:46'

        text_val_size = mock.MagicMock(name='text_size')
        text_val_size.text = '2.5G'

        td_elements = [
            text_val_name,
            text_val_size,
            text_val_datetime
        ]
        self.mock_page._url = 'https://test/url/'

        exp_result = {
            'url': 'https://test/url/testfilename.extension',
            'name': 'testfilename.extension',
            'size': '2.5G',
            'datetime': mock_datetime.strptime()
        }

        result = Page._parse_td_text_vals(self.mock_page, td_elements)
        self.assertEqual(result, exp_result)

    @mock.patch(f'{MODULE_PATH}.datetime')
    def test_parse_td_text_vals_dir(self, mock_datetime):
        """ Test _parse_td_text_vals method.
            Case: dir element.

            No test isolation for testing regex compilations.
        """
        text_val_dir = mock.MagicMock(name='text_dir')
        text_val_dir.text = 'testdir/'

        text_val_datetime = mock.MagicMock(name='text_datetime')
        text_val_datetime.text = '2019-03-16 11:46'

        td_elements = [
            text_val_dir,
            text_val_datetime
        ]
        self.mock_page._url = 'https://test/url/'

        exp_result = {
            'url': 'https://test/url/testdir/',
            'dir': 'testdir/',
            'datetime': mock_datetime.strptime()
        }

        result = Page._parse_td_text_vals(self.mock_page, td_elements)
        self.assertEqual(result, exp_result)
