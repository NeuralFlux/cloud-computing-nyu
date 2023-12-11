import logging
from opensearchpy import OpenSearch

def get_conn(host, auth):
    return OpenSearch(hosts=[host], http_auth=auth, use_ssl=True, verify_certs=True)

def create_index(client, index_name):
    index_body = {
      'settings': {
        'index': {
          'number_of_shards': 2
        }
      }
    }

    return client.indices.create(index_name, body=index_body)

def add_record(client, index_name, record):
    """
    record: JSON with bucket key and photo labels
    """
        
    response = client.index(
        index=index_name,
        body=record,
        refresh=True
    )
    
    return response

def process_lex_response(response):
    keywords = set(response['slots'].values()).difference(set([None]))
    return list(keywords)
