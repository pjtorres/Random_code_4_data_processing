import Bio.KEGG
from Bio.KEGG import REST
import argparse, re
import urllib.request
from urllib.error import HTTPError
from datetime import date
# Import Pandas, so we can use dataframes
import pandas as pd


def get_ko_hierachy(ko):
    ko_hierachy = []
    result = REST.kegg_get(ko)
    flag = False
    kodef = REST.kegg_list(ko).read()
    function_def  = kodef.split('\t')[1].split(';')[1].strip()
    for li in result:

        if flag and ('[BR:ko' in li or li[0]!=' '):

            break
        if flag:
            if ko in li:
                ko_hierachy.append([ko,function_def, l3, l2, l1])
            elif li[14] == ' ':
                l3 = li.strip('\n').strip('0123456789 ')
            elif li[13] == ' ':
                l2 = li.strip('\n').strip('0123456789 ')
            elif li[12] == ' ':
                l1 = li.strip('\n').strip('0123456789 ')

        else:
            if 'KEGG Orthology (KO)' in li:
                flag = True
    return (ko_hierachy)

