#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for general EDGAR website tasks.

EDGAR HTML specification: https://www.sec.gov/info/edgar/ednews/edhtml.htm
"""
import re

# index URL: http://www.sec.gov/Archives/edgar/data/2098/0001026608-05-000015-index.htm
# complete submission URL: http://www.sec.gov/Archives/edgar/data/2098/000102660805000015/0001026608-05-000015.txt
# Exhibit/form URL: http://www.sec.gov/Archives/edgar/data/2098/000102660815000007/acu_10k123114.htm
# ftp URL: ftp://ftp.sec.gov/edgar/data/2098/0000002098-96-000003.txt
def parse_url(url):
    """Return CIK and Accession from an EDGAR HTTP or FTP url.

    :param string url: URL from EDGAR website or FTP server.

    :return: Tuple of strings in the form (cik, accession) or (None, None)
    :rtype: tuple (string/None, string/None)
    """
    url_re = re.compile(r'/(?P<cik>\d{1,10})/'
                        r'(?P<accession>\d{10}-?\d\d-?\d{6})', re.I)
    res = url_re.search(url)
    if res:
        acc = res.group('accession')
        if len(acc) == 18:
            acc = acc[:10] + '-' + acc[10:12] + '-' + acc[12:]
        return res.group('cik'), acc
    return None, None

def get_edgar_urls(cik, accession=None):
    """Generage URLs for EDGAR FTP and HTTP sites.
    `cik` parameter can be object with `cik` and `accession` attributes or keys.

    :param string,object cik: String CIK, or object with cik and accession attributes or keys.
    :param string accession: String ACCESSION number, or None if accession in CIK object.

    :return: Tuple of strings in the form (ftp url, http url)
    :rtype: tuple (string, string)
    """
    if hasattr(cik, 'cik') and hasattr(cik, 'accession'): # cik is callable.
        accession = cik.accession if not accession else accession
        cik = cik.cik
    elif hasattr(cik, 'get') and cik.get('cik', None) and cik.get('accession', None):
        accession = cik.get('accession') if not accession else accession
        cik = cik.get('cik')

    return ('ftp://ftp.sec.gov/edgar/data/{}/{}.txt'.format(cik, accession),
            'http://www.sec.gov/Archives/edgar/data/{}/{}-index.htm'.format(cik, accession))

def edgar_links(cik, accession=None):
    """Generage HTML encoded links (using `a` tag) to EDGAR FTP and HTTP sites.
    `cik` parameter can be object with `cik` and `accession` attributes or keys.

    :param string,object cik: String CIK, or object with cik and accession attributes or keys.
    :param string accession: String ACCESSION number, or None if accession in CIK object.

    :return: String of HTTP encoded links
    :rtype: string
    """
    urls = get_edgar_urls(cik, accession=accession)

    return ("<a href='{}' target=_blank>FTP</a><a href='{}' target=_blank>HTML</a>"
            .format(*urls))
