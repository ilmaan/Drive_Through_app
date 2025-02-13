# Helper function to process input and update the order_items dictionary
import re
from pydantic import BaseModel



# Order Initialization
orders = [] 
order_items = {'burger': 0, 'fries': 0, 'drink': 0}  
order_counter = 1  




class OrderRequest(BaseModel):
    order_text: str





# FOR CANCELLATION
class CancelOrderRequest(BaseModel):
    order_no: int
    cancel_text: str  # Expecting the word "cancel"


# List to store canceled orders
canceled_orders = []




def process_order(order_text: str):
    global order_items
    
    # Initialize order items dictionary
    order_items = {'burger': 0, 'fries': 0, 'drink': 0}
    
    print("-ORDER TEXT--)()()()()()>>",order_text)
    
    item_patterns = {
        "burger": r"(\d+)\s*burger",
        "fries": r"(\d+)\s*fries",
        "drink": r"(\d+)\s*drink",
        "burgers": r"(\d+)\s*burgers",
        "drinks": r"(\d+)\s*drinks"

    }
    
    # Process each item type
    for item, pattern in item_patterns.items():
        match = re.search(pattern, order_text.lower())
        if match:
            quantity = int(match.group(1))
            if quantity > 0:
                order_items[item] = quantity
            if quantity < 0:
                return {"error": "Invalid quantity"}

    # Check for any other items not in stock 
    words = re.findall(r'\b\w+\b', order_text.lower())
    # for word in words:
    #     if word not in item_patterns and not word.isdigit():
            
    #         return {"error": f"Sorry we dont have requested items: {word} \n Please order from available items: burger, fries, or drink."}

    return order_items
