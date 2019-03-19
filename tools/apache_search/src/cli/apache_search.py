""" Module consist of main command for apache-search script.

    Functions:
        - apache_search
        - _create_table
"""
import click

from tabulate import tabulate

from tools.apache_search.src.page_search import single_page_search_files
from tools.apache_search.src.page_search import single_page_search_dirs
from tools.apache_search.src.page_search import recursive_page_search


@click.command('apache-search')
@click.option('--recursive', '-r', is_flag=True, default=False,
              help='Search for files in all nested directories.')
@click.option('--dirs', '-d', is_flag=True, default=False,
              help='Show directories only.')
@click.option('--files', '-f', is_flag=True, default=False,
              help='Show files only.')
@click.option('--display-url', '-u', is_flag=True, required=False,
              default=False, help='Show URLs only.')
@click.argument('URL')
def apache_search(url, display_url, files, dirs, recursive):
    """ Get html code from the Apache directory server (httpd),
        and search for files and directories.

        URL argument must be a full path to the directory we want to parse.

        \b
        Examples:
            - file display:
                        apache-search http://<page>/directory -f
            - directories display:
                        apache-search http://<page>/directory -d
            - full file urls display:
                        apache-search http://<page>/directory -u -f
            - files from all nested directories:
                        apache-search http://<page>/directory -r
            - full file urls from all nested directories:
                        apache-search http://<page>/directory -r -u
    """
    click.echo(f'>>>> Displaying content of: {url}')

    if files and dirs:
        raise click.ClickException(
            'Options: --files and --dirs can not be used together.'
        )

    if (recursive and files) or (recursive and dirs):
        raise click.ClickException(
            'Options: --recursive and (--files or --dirs) can not be used '
            'together. --recursive option displays only files.'
        )

    file_headers = ['Name', 'Datetime', 'Size']
    dir_headers = ['Dir', 'Datetime']

    if display_url:
        file_headers = ['Url']
        dir_headers = ['Url']

    if not recursive:
        file_list = single_page_search_files(url)
        dir_list = single_page_search_dirs(url)

        if not files and not dirs:
            files_table = _create_table(file_list, file_headers)
            click.echo('>>>> FILES')
            click.echo(files_table)

            click.echo()

            dir_table = _create_table(dir_list, dir_headers)
            click.echo('>>>> DIRECTORIES')
            click.echo(dir_table)
            click.echo()

        elif files:
            files_table = _create_table(file_list, file_headers)
            click.echo('>>>> FILES')
            click.echo(files_table)
            click.echo()

        elif dirs:
            dir_table = _create_table(dir_list, dir_headers)
            click.echo('>>>> DIRECTORIES')
            click.echo(dir_table)
            click.echo()
    else:
        files_list = recursive_page_search(url)
        files_table = _create_table(files_list, file_headers)
        click.echo('>>>> FILES')
        click.echo(files_table)
        click.echo()


def _create_table(data_list, headers):
    """ Create a table for given data list and headers.

        Args:
            data_list(list): list of dicts, which keys have to cover headers
            headers(list): list of headers for the table

        Returns:
            new_table(tabulate): created table, ready to print
    """
    list_table = list()
    for row in data_list:
        row_data = list()
        for header in headers:
            if header.lower() in row:
                row_data.append(row[header.lower()])
            else:
                row_data.append(None)

        list_table.append(row_data)
    new_table = tabulate(list_table, headers=headers)
    return new_table
