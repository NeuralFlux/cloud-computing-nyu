import json

from opensearch_utils import get_conn, create_index, add_data

INDEX_NAME = "restaurants"

if __name__ == "__main__":
    host = 'https://search-restaurants-72sydqupvni7hi2nca44i6qbz4.us-east-1.es.amazonaws.com/'
    auth = ('auth9223', 'Auth9223#')

    client = get_conn(host, auth)
    
    with open("yelp-restaurants-data.json", "r") as json_file:
        data = json.load(json_file)
    
    data = data["businesses"]
    response = add_data(client, INDEX_NAME, data)
    
    print(f"Out: {response}")
