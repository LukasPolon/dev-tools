""" Module for getting and parsing Apache directory server URL."""
import re
import os

import requests

from datetime import datetime

from bs4 import BeautifulSoup


class Page:
    """ Class for getting and parsing data from given Apache directory
        server URL. Serves list of files and directories as attributes.
    """
    def __init__(self, url):
        """ Constructor method for Page class.

            Args:
                url(str): full URL to the directory, which data
                          we want to collect
        """
        self._url = url
        self._subpages = None
        self._files = None
        self._page_bs = None

    @property
    def subpages(self):
        """ Get the subpages list as a object attribute. Loads data only
            with first use.

            Returns:
                self._subpages(list): list of dicts with subpage data
        """
        if self._subpages is None:
            self._subpages = self._get_subpages()
        return self._subpages

    @property
    def files(self):
        """ Get the file list as a object attribute. Loads data only
            with first use.

            Returns:
                self._files(list): list of dicts with file data
        """
        if self._files is None:
            self._files = self._get_files()
        return self._files

    def _get_raw_page(self):
        """ Get raw html page code from GET request.

            Returns:
                raw_page(str): page html code

            Raises:
                ConnectionError: if GET request returns exit code
                                 different than 200
        """
        request_result = requests.get(self._url)
        if not request_result.status_code == 200:
            raise ConnectionError(
                f'Can not connect to: {self._url}. '
                f'Status code: {request_result.status_code}'
            )
        raw_page = request_result.text
        return raw_page

    def _get_bs(self):
        """ Get BeautifulSoup object from the page raw html code.

            Returns:
                self._page_bs(BeautifulSoup): bs4 object
        """
        if self._page_bs is None:
            raw_page = self._get_raw_page()
            self._page_bs = BeautifulSoup(raw_page, 'html.parser')
        return self._page_bs

    def _get_files(self):
        """ Parse html output to get a list of files.
            Each file is described by the dictionary with given keys:
            - name: file name
            - url: full URL to the file
            - datetime: file last modification date in datetime.datetime format
            - size: file size in format: X (bytes), XM (megabytes),
                                         XG (gigabytes)

            Warning: if some of the parameters are missing in the html output,
                     they will not appear in the dictionary.

            Returns:
                files(list): list of dictionaries - file data
        """
        soup_url = self._get_bs()
        files = list()
        table_elements = soup_url.find_all('tr')
        for table_element in table_elements:
            td_elements = table_element.find_all('td')
            alt_elements = self._find_alt_elements('files', td_elements)

            if any(alt_elements):
                file = self._parse_td_text_vals(td_elements)
                if file:
                    files.append(file)
        return files

    def _get_subpages(self):
        """ Parse html output to get a list of directories (subpages).
            Each directory is described by the dictionary with given keys:
            - name: directory name
            - url: full URL to the directory
            - datetime: directory last modification date in
                        datetime.datetime format

            Warning: if some of the parameters are missing in the html output,
                     they will not appear in the dictionary.

            Returns:
                subpages(list): list of dictionaries - directory data
                """
        soup_url = self._get_bs()
        subpages = list()
        table_elements = soup_url.find_all('tr')
        for table_element in table_elements:
            td_elements = table_element.find_all('td')
            alt_elements = self._find_alt_elements('dirs', td_elements)

            if any(alt_elements):
                subpage = self._parse_td_text_vals(td_elements)
                if subpage:
                    subpages.append(subpage)
        return subpages

    def _find_alt_elements(self, target, td_elements):
        """ Find "img alt" html elements and check if they have correct
            string, according to the target, which is file or directory.

            This is a way to check if given html table row (td elements,
            which are table cells in a single row) contains file or directory.

            Args:
                target(str): can be "files" or "dirs"
                td_elements(BeautifulSoup): html table cells in a single row

            Returns:
                alt_elements(list): list of filtered "alt" elements
        """
        alt_regex = re.compile(r'\[([A-Z ]+)\]')
        alt_elements = [el.find(alt=alt_regex) for el in td_elements]

        if target == 'files':
            alt_exclusions = ['[ICO]', '[PARENTDIR]', '[DIR]']
            alt_elements = [el for el in alt_elements
                            if el and el.attrs['alt']
                            not in alt_exclusions]
        if target == 'dirs':
            alt_elements = [el for el in alt_elements
                            if el and el.attrs['alt'] == '[DIR]']
        return alt_elements

    def _parse_td_text_vals(self, td_elements):
        """ Parse html table cells from one row, to get the elements:
            - name: file name
            - dir: directory name
            - datetime: file/directory last modification date
            - size: file size
            - url: full url to the file/directory

            Files can have name, datetime and size elements.
            Directories can have dir and datetime elements.

            Datetime element is converted to the datetime.datetime object,
            with given structure: "year-month-day hour-minutes"

            Element values came from text values found in cells in row.

            Args:
                td_elements(BeautifulSoup): html table cells in one row

            Returns:
                item(dict): dictionary with file/directory info
        """
        text_vals = [text_val.text.strip() for text_val in td_elements
                     if text_val.text]
        rules = {
            'name': re.compile(r'[a-zA-Z0-9\-_\.></]+\.[a-zA-Z0-9\-_\.]+'),
            'dir': re.compile(r'[a-zA-Z0-9\-_\.><]+/\Z'),
            'datetime': re.compile(r'\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}'),
            'size': re.compile(r'\d+\.?\d*[GM]?\Z')
        }

        item = dict()
        for text_element in text_vals:
            for rule_name, rule in rules.items():
                if rule.match(text_element):
                    if rule_name == 'datetime':
                        text_element = datetime.strptime(
                            text_element,
                            '%Y-%m-%d %H:%M'
                        )
                    if rule_name in ['name', 'dir']:
                        element_url = os.path.join(
                            self._url,
                            text_element
                        )
                        item['url'] = element_url
                    item[rule_name] = text_element
                    del rules[rule_name]
                    break
        return item
