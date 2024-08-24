import requests

root_endpoint = "http://localhost:8080"
items_endpoint = root_endpoint + "/items"

test_api_index = requests.get(root_endpoint).json()
print()

print(test_api_index)

test_api_items = requests.get(items_endpoint).json()
print(test_api_items)
print()

test_api_item_1 = requests.get(f"{items_endpoint}/1").json()
test_api_item_6 = requests.get(f"{items_endpoint}/7").json()
test_api_item_fasdf = requests.get(f"{items_endpoint}/ffad").json()

print(test_api_item_1)
print(test_api_item_6)
print(test_api_item_fasdf)
print()

test_api_items_query = requests.get(
    f"{items_endpoint}-query?name=Nails").json()
print(test_api_items_query)

print()
print("Adding an item")
test_add_item = requests.post(
    items_endpoint,
    json={"name": "Screwdriver", "price": 3.99,
          "count": 10, "id": 5, "category": "tools"}
).json()

print(test_add_item)
test_api_items = requests.get(items_endpoint).json()

print(test_api_items)

print("Updating an item")
print(requests.put(f"{items_endpoint}/0?count=150").json())
print(requests.get(items_endpoint).json())
print()
