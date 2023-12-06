## Scraping Yelp Data
We use the [Yelp API](https://docs.developer.yelp.com/reference/v3_business_search) to fetch relevant restaurants.

cURL command is as follows
```
curl --request GET \
     --url 'https://api.yelp.com/v3/businesses/search?location=manhattan&term=PREFERRED_CUISINE%20restaurant&sort_by=best_match&limit=50' \
     --header 'Authorization: GKKitBSpFNXAid9V9F_8HlOVZl_ghP_P613nVcaP6fQJ73n7ZqwkUmrYLn4YE1JKvyxF9RbqJjCIY8x7guZq2hrwW-egabE6vZpDDNgcefs_dkwK7T3ZxA7lFkUsZXYx' \
     --header 'accept: application/json'
```
