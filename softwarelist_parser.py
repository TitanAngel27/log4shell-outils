import csv as py_csv
import sys
import json as py_json
import pathlib
import tempfile

from typing import List

import click
import mistune
import requests
import unicodedata

from bs4 import BeautifulSoup
from bs4.element import Tag

from datetime import date

HEADERS = [
    'Supplier',
    'Product',
    'Version',
    'Status CVE-2021-4104',
    'Status CVE-2021-44228',
    'Status CVE-2021-45046',
    'Status CVE-2021-45105',
    'Notes',
    'Links'
]

def download_softwarelist() -> str:
    """ Download softwarelist to parse

    :return: Markdown content of software list
    """
    url = "https://raw.githubusercontent.com/NCSC-NL/log4shell/main/software/README.md"
    response = requests.get(url)
    return response.content

def parse_links(links: List[Tag] = None) -> dict:
    """ Get all links info from Links column

    :return: Dictionary with `{link_text: link_href}`
    """
    return {link.text: link.get('href') for link in links}

def parse_record(record: List[Tag] = None) -> dict:
    """ Parse single tr record in Software list

    :return: Dictionary of parsed cell from record
    """

    result = dict()

    for index, header in enumerate(HEADERS):
        # Parse links differently
        if index == 8:
            if len(record) == 8:
                result[header] = {}
            else:
                result[header] = parse_links(record[index].find_all('a'))

        else:
            # Ensure unicode in text is properly parsed
            result[header] = unicodedata.normalize("NFKD", record[index].text)

    return result

@click.group()
#@click.option('--path', default='./README.md', help='Path to software list README.md', type=click.File(encoding='UTF-8'))#Specifier Encoding
@click.pass_context
def main(ctx):

    # Parse Markdown to HTML and get soup
    #content = path.read()
    content = download_softwarelist()
    html = mistune.html(content.decode('utf-8'))
    soup = BeautifulSoup(html, 'html.parser')

    # Look for all tr columns with td fields, after first h3 header
    records = list()
    first_h3 = soup.find('h3')

    for x in first_h3.next_elements:
        if isinstance(x, Tag) and x.name == 'tr':
            tds = x.find_all('td')

            if tds:  # ensure empty tr are ignored
                records.append(parse_record(tds))

    ctx.obj['records'] = records


@main.command()
@click.argument('output', default='-', type=click.File('w+'))
@click.pass_context
def json(ctx, output):
    py_json.dump(ctx.obj['records'], output)

@main.command()
#@click.argument('output', default='list.csv', type=click.File('w+',encoding='UTF-8'))
@click.pass_context
def csv(ctx):#, output):
    #Ajout HEADER pour la daate de derniere MAJ
    #HEADERS.append('Date MAJ')

    current_day = date.today()

    nomcsv = '.\Liste\list_log4shell_'+str(current_day.month)+'-'+str(current_day.day)+'.csv'

    with open(nomcsv, 'w+', encoding='UTF-8', newline='') as csvfile:
        writer = py_csv.DictWriter(csvfile, HEADERS, delimiter=';')

        writer.writeheader()

        # cleanup links
        for record in ctx.obj['records']:
            record['Links'] = list(record['Links'].values())

            #ADD date record
            #record['Date MAJ'] = date.today()

            writer.writerow(record)


if __name__ == '__main__':
    main(obj={})
