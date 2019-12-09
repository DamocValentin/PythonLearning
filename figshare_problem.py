import hashlib
import json
import os
import xml.etree.ElementTree as ET
import requests
from requests.exceptions import HTTPError

BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
TOKEN = '858b1761d543afd8ffde2a29169b1c375fa498f5b2e6496ad444e863494a05472a79a4efcf7d064b3f0f55bdb4aa4a4e1a27155219e16b0bb898f9f55308f491'
CHUNK_SIZE = 1048576


FILE_PATH_XML = 'lit_dspace_export\\23\dublin_core.xml'
FILE_PATH_PDF = 'lit_dspace_export\\23\\locationidentitysingetal.pdf'


def raw_issue_request(method, url, data=None, binary=False):
    headers = {'Authorization': 'token ' + TOKEN}
    if data is not None and not binary:
        data = json.dumps(data)
    response = requests.request(method, url, headers=headers, data=data)
    try:
        response.raise_for_status()
        try:
            data = json.loads(response.content)
        except ValueError:
            data = response.content
    except HTTPError as error:
        print('Caught an HTTPError: {}'.format(error))
        print('Body:\n', response.content)
        raise

    return data


def issue_request(method, endpoint, *args, **kwargs):
    return raw_issue_request(method, BASE_URL.format(endpoint=endpoint), *args, **kwargs)


def get_article_data(path):
    xml_data = dict()

    xml_tree = ET.parse(path)
    root = xml_tree.getroot()

    authors_list = list()
    categories_list = list()
    keywords_list = list()

    for child in root:
        child_attrib = child.attrib

        if child_attrib['element'] == 'title' and child_attrib['qualifier'] == 'none':
            xml_data['title'] = child.text

        elif child_attrib['element'] == 'subject' and child_attrib['qualifier'] == 'for':
            category_id = find__category(child.text)
            if category_id is not None:
                categories_list.append(category_id)

        elif child_attrib['element'] == 'subject' and child_attrib['qualifier'] == 'keyword':
            keywords_list.append(child.text)

        elif child_attrib['element'] == 'description' and child_attrib['qualifier'] == 'abstract':
            xml_data['description'] = child.text

        elif child_attrib['element'] == 'contributor' and child_attrib['qualifier'] == 'author':
            author_data = dict()
            author_data["search_for"] = child.text
            author_details = find_author(author_data)
            if author_details != {}:
                authors_list.append(find_author(author_data))

        elif child_attrib['element'] == 'rights' and child_attrib['qualifier'] == 'none':
            xml_data['licence'] = child.text

        elif child_attrib['element'] == 'type' and child_attrib['qualifier'] == 'none':
            xml_data['defined_type'] = child.text

    xml_data['authors'] = authors_list
    xml_data['categories'] = categories_list
    xml_data['keywords'] = keywords_list

    return xml_data


def create_article(data):
    result = issue_request('POST', 'account/articles', data=data)
    result = raw_issue_request('GET', result['location'])

    return result['id']


def find_author(data):
    result = issue_request('POST', 'account/authors/search', data=data)
    return_data = {}
    for author in result:
        if data['search_for'] == author['full_name']:
            return_data['name'] = author['full_name']
            return_data['id'] = author['id']

    return return_data


def delete_author(article_id, author_name):
    author_data = dict()
    author_data["search_for"] = author_name
    author = find_author(author_data)
    issue_request('DELETE', 'account/articles/{}/authors/{}'.format(article_id, author['id']))


def find__category(data):
    categories = issue_request('GET', 'categories')
    for category in categories:
        if category['title'] == data:
            return category['id']
    return None


def get_file_check_data(file_name):
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(CHUNK_SIZE)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(CHUNK_SIZE)
        return md5.hexdigest(), size


def initiate_new_upload(article_id, file_name):
    endpoint = 'account/articles/{}/files'
    endpoint = endpoint.format(article_id)

    md5, size = get_file_check_data(file_name)
    data = {'name': os.path.basename(file_name),
            'md5': md5,
            'size': size}

    result = issue_request('POST', endpoint, data=data)

    result = raw_issue_request('GET', result['location'])

    return result


def upload_parts(file_info):
    url = '{upload_url}'.format(**file_info)
    result = raw_issue_request('GET', url)

    with open(FILE_PATH_PDF, 'rb') as fin:
        for part in result['parts']:
            upload_part(file_info, fin, part)


def upload_part(file_info, stream, part):
    udata = file_info.copy()
    udata.update(part)
    url = '{upload_url}/{partNo}'.format(**udata)

    stream.seek(part['startOffset'])
    data = stream.read(part['endOffset'] - part['startOffset'] + 1)

    raw_issue_request('PUT', url, data=data, binary=True)


def complete_upload(article_id, file_id):
    issue_request('POST', 'account/articles/{}/files/{}'.format(article_id, file_id))


def main():
    # Gather article data
    article_data = get_article_data(FILE_PATH_XML)

    # Create article
    article_id = create_article(article_data)

    # Delete my ownership on the article
    delete_author(article_id, 'Valentin Damoc')

    # Upload file for article
    file_info = initiate_new_upload(article_id, FILE_PATH_PDF)
    upload_parts(file_info)

    # Complete process
    complete_upload(article_id, file_info['id'])


if __name__ == '__main__':
    main()
