# Store APIs Design
## Collections
1. collections/
	**GET**
	Get whole list of all available collections
	```json
		{
			'id': 1, // <int> 
			'title': 'name', // <string> name of the collection
			'featured_products': [{ 'id': 1, 'title': 'product1', 'unit_price': 1}] 
			// <List> List of products
		}
	```
	**PATCH**
	```json
		{
			'title': 'example', // (Required)<str> name of the collection
			'featured_product_ids': [1, 2] // (Optional)<List> list of ids belong to the collection
		}
	```
2. collections/{id}
	**GET**
	Get collection details regarding to a specific id
	**PATCH**
	```json
	{
		'title': 'example', // (Required)<str> name of the collection
		'featured_product_ids': [1, 2] // (Optional)<List> list of ids belong to the collection
	}
	```
	**DELETE**
	Delete a collection
