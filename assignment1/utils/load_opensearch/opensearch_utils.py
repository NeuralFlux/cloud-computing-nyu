from opensearchpy import OpenSearch

def get_conn(host, auth):
    return OpenSearch(hosts=[host], http_auth=auth, use_ssl=True, verify_certs=True)

def create_index(client, index_name, body):
    return client.indices.create(index_name, body=body)

def add_data(client, index_name, data):
    """
    data: JSON with each record as a restaurant
    """
    
    counter = 1
    for restaurant in data:
        record = {
            "restaurant": {
                "restaurant_id": restaurant["id"],
                "cuisine": restaurant["cuisine"]
            }
        }
        
        response = client.index(
            index=index_name,
            body=record,
            id=restaurant["id"],
            refresh=True
        )
        
        print(f"[{counter}] RESP {response} for INSERT {record}")
        counter += 1
