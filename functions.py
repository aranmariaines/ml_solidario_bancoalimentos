# Functions used in get_data.py
import requests

def get_item(item_code):
    """
	Get data about an item

	Parameters:
	----------
	item_code : string
		It is in the url in the browser, for example MLA817804577.
	Returns:
	-------
		json with items attributes
	"""
    r = requests.get(f"https://api.mercadolibre.com/items/{item_code}#json") 
    return r.json()

# Get all the items from seller
def get_all_items_from_seller(seller_id):
    """
	Get data about a seller

	Parameters:
	----------
	seller_id : int.
		Id for the seller, can be found in the json returned by get_item
	Returns:
	-------
		json with seller attributes
	"""
    items = requests.get(f'https://api.mercadolibre.com/sites/MLA/search?seller_id={seller_id}')
    return items.json()

# Get Questions
def get_questions_about_item(item_id,access_token):
    """
	Get questions and answers on an item

	Parameters:
	----------
	item_code : string
		It is in the url in the browser, for example MLA817804577
	access_token : string
		Credential to access private data in Mercado Libre. 
	Returns:
	-------
		json with questions and answers on an item
	"""
    questions = requests.get(f"https://api.mercadolibre.com/questions/search?item={item_id}&access_token={access_token}")
    return questions.json()

# Quantity of visitas (hacer un loop para bajar diario)
def get_total_visits(user_id,date_from,date_to):
    """
	Get total visits for all the items of a seller

	Parameters:
	----------
	user_id : int
		Same as seller ir. It can be found in the json returned by get_item
	date_from : string
		Beginning date and time. It follows this format: '2019-12-02T15:45:47.000Z' 
	date_to: string
		Ending date and time. It follows this format: '2019-12-02T15:45:47.000Z' 
	Returns:
	-------
		json with total visits for the seller
	"""
    visits = requests.get(f"https://api.mercadolibre.com/users/{user_id}/items_visits?date_from={date_from}&date_to={date_to}")
    return visits.json()

# Visits per item
def get_visits_per_item(item_id,last,unit):
    """
	Get total visits for an item

	Parameters:
	----------
	item_id : string
		Item code. It is in the url in the browser, for example MLA817804577
	last : int
		Quantity units to consider before the moment where the script is run
	unit : string
		Unit of time: month,days,hours.
	Returns:
	-------
		json with total visits per item and attributes
	"""
    visits_item = requests.get(f"https://api.mercadolibre.com/items/{item_id}/visits/time_window?last={last}&unit={unit}")
    return visits_item.json()

# Branding
def get_brand_info(user_id):
    """
	Get info on the seller and the brand

	Parameters:
	----------
	user_id : int
		Same as seller ir. It can be found in the json returned by get_item
	Returns:
	-------
		json with attributes of brand and seller including images.
	"""
    brands = requests.get(f"https://api.mercadolibre.com/users/{user_id}/brands")
    return brands.json()

# Feedback on items 
def get_feedback_on_item(item_id):
    """
	Get feedback and user's opinions after purchasing an item

	Parameters:
	----------
	item_id : string
		Item code. It is in the url in the browser, for example MLA817804577
	Returns:
	-------
		json with attributes such as rating and text for an item
	"""
    feedback = requests.get(f"https://api.mercadolibre.com/reviews/item/{item_id}")
    return feedback.json()


