# -*- coding: utf-8 -*-

import logging
import os
import re

import requests

log = logging.getLogger(__name__)


def is_file(value, rule_obj, path):
    if os.path.isfile(value):
        return True
    raise Exception("Path {} is not a file".format(value))


def is_dir(value, rule_obj, path):
    if os.path.isdir(value):
        return True
    raise Exception("Path {} is not a directory".format(value))


def is_valid_name(value, rule_obj, path):
    # Only accept alphanumericals & - & _
    if re.match(r'^[A-Za-z0-9_-]+$', value):
        return True
    raise Exception("Name {} is not a valid internal name".format(value))


def ext_onto_organism(value, rule_obj, path):
    log.debug("value: %s", value)
    log.debug("rule_obj: %s", rule_obj)
    log.debug("path: %s", path)
    # TODO: Better management when EBI is down
    return True
    # return _validate_ontological_term(value, "NCBITAXON")


def _validate_ontological_term(term, ontology, root_term_iri=""):
    base_path = "http://www.ebi.ac.uk/ols/api/search"
    body = {
        "q": term,
        "ontology": ontology.lower(),
        "type": "class",
        "exact": True,
        "queryFields": ["label", "synonym"]
    }
    if root_term_iri:
        body["childrenOf"] = root_term_iri
    r = requests.get(base_path, params=body)
    res = r.json()

    log.info(res["response"])
    if not res["response"]["numFound"] == 1:
        return 'Term {} not found in ontology {}'.format(term, ontology)
    return True
