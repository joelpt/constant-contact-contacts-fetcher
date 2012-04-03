#!/usr/bin/python

import xml.dom.minidom
import httplib2
import csv
import sys
import logging
import optparse


def get_node_value(node, innerTagName):
    inner_node = node.getElementsByTagName(innerTagName)[0].firstChild
    if inner_node is None:
        return u''
    else:
        return inner_node.data


def parse_contacts_page(content):

    contacts = []
    doc = xml.dom.minidom.parseString(content)
    entries = doc.getElementsByTagName('entry')

    for entry in entries:
        contact = entry.getElementsByTagName('Contact')[0]
        contacts += [(
            get_node_value(contact, 'Status'),
            get_node_value(contact, 'Name'),
            get_node_value(contact, 'EmailAddress')
        )]

    nexturl = None
    links = doc.getElementsByTagName('link')
    for link in links:
        if link.hasAttribute('rel'):
            if link.getAttribute('rel') == 'next':
                nexturl = link.getAttribute('href')

    return nexturl, contacts


def get_contacts(cc_api_key, cc_username, cc_password):
    contacts = []

    # we disable certificate validation to avoid SSL headaches on Windows
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    h.add_credentials(cc_api_key + '%' + cc_username, cc_password)

    baseurl = 'https://api.constantcontact.com'
    url = baseurl + '/ws/customers/%s/contacts' % \
        cc_username
    logging.info('Starting with url: ' + url)

    while True:
        content = h.request(url, 'GET')[1]
        nexturl, newcontacts = parse_contacts_page(content)
        contacts += newcontacts
        logging.info('%d contacts retrieved' % len(contacts))
        if nexturl is not None:
            url = baseurl + nexturl
        else:
            break

    return contacts


def run(cc_api_key, cc_username, cc_password, csv_file):
    contacts = get_contacts(cc_api_key, cc_username, cc_password)
    # contacts = get_contacts('253ade64-a623-4d58-a4e9-4f7cb6c7265d', 'ayurvedaseattle',
    #     'ganesha108')

    writer = csv.writer(csv_file)

    writer.writerow(('Status', 'Name', 'EmailAddress'))
    for c in contacts:
        writer.writerow(c)

    logging.info('Wrote %d contacts.' % len(contacts))


if __name__ == "__main__":
    usage = "usage: %prog [options] <cc_api_key> <cc_username> <cc_password> [csv_file]"
    description = "Retrieve all contacts from a Constant Contact account and output in CSV format."
    parser = optparse.OptionParser(usage=usage, description=description)
    parser.add_option('-n', '--noprogress', action="store_true", dest="noprogress", help="Don't print progress messages to stdout", default=False)
    options, args = parser.parse_args()

    if len(args) < 3 or len(args) > 4:
        parser.print_help()
        sys.exit()

    cc_api_key, cc_username, cc_password = args[0:3]

    if len(args) == 4:
        csv_file = open(args[3], 'wb')
    else:
        csv_file = sys.stdout

    if not options.noprogress:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        run(cc_api_key, cc_username, cc_password, csv_file)
    except:
        parser.print_help()
        raise
