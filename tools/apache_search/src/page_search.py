""" Module responsible for encapsulating logic to use in the cli modules."""
from tools.apache_search.src.page import Page


def single_page_search_files(url):
    """ Get list of files from the given url.

        Args:
            url(str): full url to the page

        Returns:
            file_list(list): list of the files data
    """
    page = Page(url)
    file_list = page.files
    return file_list


def single_page_search_dirs(url):
    """ Get list of directories from the given url.

            Args:
                url(str): full url to the page

            Returns:
                dir_list(list): list of the directories data
        """
    page = Page(url)
    dir_list = page.subpages
    return dir_list


def recursive_page_search(url):
    """ Get list of files from given url, and all directories below.

        Args:
            url(str): full url to the page

        Returns:
            files(list): list of the files data
    """
    pages = [Page(url)]
    files = list()

    while pages:
        page = pages.pop()
        files += page.files
        for subpage in page.subpages:
            pages.append(Page(subpage['url']))

    return files
