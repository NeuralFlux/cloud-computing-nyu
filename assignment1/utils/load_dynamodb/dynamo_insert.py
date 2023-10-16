import json
import boto3
import time
import decimal

def format_record(restaurant):
    item = {
        "restaurant_id": restaurant["id"],
        "insertion_timestamp": time.time_ns(),
        "name": restaurant["name"],
        "address": restaurant["location"],
        "coordinates": restaurant["coordinates"],
        "review_count": restaurant["review_count"],
        "rating": restaurant["rating"],
        "zip_code": restaurant["location"]["zip_code"]
    }

    return item


if __name__ == "__main__":
    dynamo_client = boto3.resource("dynamodb")
    restaurants_table = dynamo_client.Table("yelp-restaurants")

    cuisines = ["indian", "chinese", "italian"]

    for cuisine in cuisines:
        with open(f"{cuisine}.json", "r") as json_file:
            restaurants = json.load(json_file)
        
        for restaurant in restaurants["businesses"]:
            item = format_record(restaurant)

            dynamodb_item = json.loads(
                json.dumps(item), parse_float=decimal.Decimal
            )

            response = restaurants_table.put_item(Item=dynamodb_item)
            assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
            print(f"INSERT {cuisine} {item['restaurant_id']}")

            time.sleep(2.0)
