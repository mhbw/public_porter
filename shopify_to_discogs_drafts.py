# The script here works on the asumption that you have a private App and developer's key
## and that you have authenticated it. The guide on how to set up a private App is in the 
## url here: https://help.shopify.com/en/manual/apps/app-types/custom-apps

import urllib3
import shopify 
import requests
import os
import json
from requests_oauthlib import OAuth1
from prefect import flow, task

## store more safely - mw 8/6/2025

SHOPIFY_ACCESS_TOKEN = 'your_shopify_token'
SHOPIFY_STORE_NAME = 'your_shopify_storename' # note: this is in the url slug. it's not your registered business name.

DISCOGS_TOKEN = 'your_discogs_token'
## simple function to test getting orders and saving them 
## print out to test
## this could be made more robust by first looking to confirm that the API call worked
## I had originally written in a loop that checked for a 200 response and removed it
## also, in other context, you may care about quantity of albums. In this case all SKUs
## are 1 of 1, so we don't have to add that QC in. 

def order_fetch(store_name, access_token):
    SHOPIFY_ORDER_URL = f"https://{store_name}.myshopify.com/admin/api/2021-04/orders.json?status=OPEN"
    headers = { "X-Shopify-Access-Token": access_token}
    shopify_response = requests.get(SHOPIFY_ORDER_URL, headers=headers)
        
    if shopify_response.status_code == 200:
        shopify_orders = shopify_response.json().get('orders', [])
        skus = [
            item.get('sku')
            for order in shopify_orders
            for item in order.get('line_items', [])
            if item.get('sku')
        ]
        return skus

skus = order_fetch(SHOPIFY_STORE_NAME, SHOPIFY_ACCESS_TOKEN)

print(skus)

## function takes the list of skus and the Discogs Token and checks if they exist
## if they do, it sets them to draft. 
## working as of 8/14/25 

def set_listing_to_draft(token: str, listing_id: int) -> dict:
    base_url = f"https://api.discogs.com/marketplace/listings/{listing_id}"
    params = {"token": token}

    get_resp = requests.get(base_url, params=params)
    if get_resp.status_code != 200:
        return {"error": "Failed to fetch listing", "status_code": get_resp.status_code, "body": get_resp.text}

    listing_data = get_resp.json()
    listing_data["status"] = "Draft"

    post_resp = requests.post(base_url, params=params, json=listing_data)
    return {
        "status_code": post_resp.status_code,
        "response": post_resp.text.strip()
    }


results = set_listings_to_draft(DISCOGS_TOKEN, skus)
for r in results:
    print(r)

