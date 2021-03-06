#!/usr/bin/env python
# encoding: utf-8
"""
Snappy documentation goes here
@author: Heather Piwowar
@contact:  hpiwowar@gmail.com
@status:  playing around
"""

import sys
import os
import nose
from nose.tools import assert_equals
from tests import slow, online, notimplemented, acceptance
import dataset
import datasources
from datasources import scirus
from utils.cache import TimedCache

if __name__ == '__main__':
    nose.runmodule()
    
def get_this_dir():
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)
        
# Shared test data
gold_query = """((pcr+AND+activity)+OR+(rna+AND+amplified))"""
gold_first_url = """http://www.scirus.com/srsapp/search?sort=0&t=all&q=((pcr+AND+activity)+OR+(rna+AND+amplified))+(journal%3Acell+OR+journal%3Ascience+OR+journal%3ANature)&cn=all&co=AND&t=any&q=microarray*+%22genome-wide%22+%22expression+profile*%22+++%22transcription+profil*%22&cn=all&fdt=2007&tdt=2007&g=a&dt=all&ff=all&ds=jnl&ds=nom&ds=web&sa=all&p=0"""
gold_next_url = """http://www.scirus.com/srsapp/search?sort=0&t=all&q=((pcr+AND+activity)+OR+(rna+AND+amplified))+(journal%3Acell+OR+journal%3Ascience+OR+journal%3ANature)&cn=all&co=AND&t=any&q=microarray*+%22genome-wide%22+%22expression+profile*%22+++%22transcription+profil*%22&cn=all&fdt=2007&tdt=2007&g=a&dt=all&ff=all&ds=jnl&ds=nom&ds=web&sa=all&p=101"""
gold_first_filename = os.path.join(get_this_dir(), 'testdata', 'scirus_gold_results.html')
gold_next_filename = os.path.join(get_this_dir(), 'testdata', 'scirus_gold_results_101.html')
gold_first_page = open(gold_first_filename, "r").read()
gold_next_page = open(gold_next_filename, "r").read()
gold_first_DOIs = ['10.1038/nprot.2007.187', '10.1038/sj.cdd.4402209', '10.1038/sj.cdd.4402067', '10.1186/1475-2867-7-14', '10.1038/sj.cdd.4402227', '10.1038/nmeth977', '10.1186/1475-2859-6-37', '10.1186/1475-2859-6-32', '10.1186/1475-2859-6-30', '10.1186/1471-2121-8-51', '10.1038/nsmb1249', '10.1038/nsmb1209', '10.1088/1009-0630/9/5/24', '10.1038/nmeth1007-869', '10.1038/cr.2007.1', '10.1038/nsmb0307-174', '10.1038/nprot.2007.457', '10.1038/sj.cdd.4402123', '10.1038/sj.cdd.4401990', '10.1186/1475-2859-6-24', '10.1186/1475-2859-6-29', '10.1038/cr.2007.40', '10.1038/nmeth946']
gold_first_citations = ['Cell|2007|131|706||test', 'Molecular Cell|2007|27|393||test', 'Cell|2007|131|1273||test', 'Developmental Cell|2007|12|57||test', 'Journal of Dermatological Science|2007|47|201||test']
gold_first_PMIDs = ['18079713', '18047638', '18039355', '17932503', '17927824', '17880710', '17845729', '17762884', '17725816', '17692125', '17486124', '17486099', '17363962', '17334403', '17310252', '17287829', '17170753', '17115035', '17099705', '16794603']

class TestScirus(object):

    def test_get_first_url_from_query(self):
        url = scirus.get_url_from_query(gold_query)
        assert_equals(url, gold_first_url)

        url = scirus.get_url_from_query(gold_query, 101)
        assert_equals(url, gold_next_url)

    def test_get_page_from_url(self):
        first_page = scirus.get_page_from_url(gold_first_url)
        assert_equals(first_page[0:1000], gold_first_page[0:1000])

        next_page = scirus.get_page_from_url(gold_next_url)
        assert_equals(next_page[0:1000], gold_next_page[0:1000])

    def test_get_DOIs_from_page(self):
        DOIs = scirus.get_DOIs_from_page(gold_first_page)
        assert_equals(DOIs, gold_first_DOIs)

    def test_get_citations_from_page(self):
        items_dict = scirus.get_citations_from_page(gold_first_page)
        lookup_lines = scirus.convert_items_to_lookup_strings(items_dict)
        assert_equals(lookup_lines[0:5], gold_first_citations)

    def test_get_PMIDs_from_DOIs(self):
        PMIDs = scirus.get_PMIDs_from_DOIs(gold_first_DOIs)
        assert_equals(PMIDs, gold_first_PMIDs)
    
    def test_get_citation_file_from_pages_in_directory(self):
        glob_pattern = os.path.join(get_this_dir(), 'testdata', 'scirus', "*", "*.html")
        list_of_citation_strings = scirus.get_citations_from_directories(glob_pattern, "scirus;")
        for str in list_of_citation_strings[0:10]:
            print str
        assert_equals(len(list_of_citation_strings), 199)
        assert_equals(list_of_citation_strings[0:5], ['Molecular Cell|2007|27|393||scirus;predef_all', 'Nature Methods|2007|4|87||scirus;predef_all', 'Cell|2007|131|831||scirus;predef_all', 'Cell|2007|131|405||scirus;predef_all', 'Molecular Cell|2007|27|890||scirus;predef_all'])


        
    