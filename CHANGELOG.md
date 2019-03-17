<!---
#######################################
## Dev-tools Changelog
##
## Format: markdown (md)
## Latest versions should be placed as first
##
## Notation: 00.01.02
##      - 00: stable released version
##      - 01: new features
##      - 02: bug fixes and small changes 
##
## Updating schema (mandatory):
##      <empty_line>
##      <version> (dd/mm/rrrr)
##      ----------------------
##      * <item>
##      * <item>
##      <empty_line>
##
## Useful tutorial: https://en.support.wordpress.com/markdown-quick-reference/
##
#######################################
-->
00.01.02 (17/02/2019)
---------------------
* Added: unit tests for apache_search.src.cli.apache_search module

00.01.01 (16/02/2019)
---------------------
* Added: unit tests for page.py and page_search.py modules
* Changed: .travis.yml to run coverage, coveralls and pylint

00.01.00 (15/02/2019)
---------------------
* Added: apache-search command is implemented for single page search
* Changed: .pylintrc customization
* Changed: requirements.txt - pylint, click, bs4, requests, tabulate added


00.00.01 (03/03/2019)
---------------------
* Added: project created
* Added: configuration files for pylint, hound, coverage, requirements, travis
* Added: tools, networking packages
* Added: ssh_manager initial module