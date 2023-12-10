import logging
from opensearchpy import OpenSearch

def get_conn(host, auth):
    return OpenSearch(hosts=[host], http_auth=auth, use_ssl=True, verify_certs=True)

def create_index(client, index_name, body):
    return client.indices.create(index_name, body=body)

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
