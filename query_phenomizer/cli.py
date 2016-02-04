#!/usr/bin/env python
# encoding: utf-8
"""
query_phenomizer

Command line script for query phenomizer database.

Created by Måns Magnusson on 2015-02-02.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""
from __future__ import print_function

import sys
import os
import click

from pprint import pprint as pp

from query_phenomizer import query, validate_term

@click.command()
@click.option('-t', '--hpo_term',
                multiple=True,
                help="Give hpo terms either on the form 'HP:0001623', or '0001623'"
)
@click.option('-c', '--check_terms',
                is_flag=True,
                help="Check if the term(s) exist"
)
@click.option('-o', '--output',
                    type=click.File('wb'),
                    help="Specify the path to a file for storing the phenomizer output."
)
@click.option('-p', '--p_value_limit',
                    nargs=1,
                    default=1.0,
                    help='Specify the highest p-value that you want included.'
)
@click.option('-v', '--verbose', 
                is_flag=True,
                help='Increase output verbosity.'
)
def query_phenomizer(hpo_term, check_terms, output, p_value_limit, verbose):
    if not hpo_term:
        print("Please specify at least one hpo term with '-t/--hpo_term'.", file=sys.stderr)
        sys.exit()
    
    hpo_list = []
    for term in hpo_term:
        if len(term.split(':')) < 2:
            term = ':'.join(['HP', term])
        hpo_list.append(term)
    
    if verbose:
        print("HPO terms used: %s." % ','.join(hpo_list) , file=sys.stderr)
    
    if check_terms:
        for term in hpo_term:
            if not validate_term(term):
                print("HPO term : %s does not exist." % term , file=sys.stderr)
    
    results = query(hpo_list)
    
    nr_significant_genes = 0
    for result in results:
        if result['p_value'] < p_value_limit:
            nr_significant_genes += 1
            if output:
                # print(result['raw_line'])
                output.write(result['raw_line'] + '\n')
            else:
                pp(result)
    
    if nr_significant_genes == 0:
        if verbose:
            print("There where no significant genes with p value < %s"
                    % p_value_limit, file=sys.stderr)

if __name__ == '__main__':
    query_phenomizer()
