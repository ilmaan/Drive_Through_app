from fastapi import FastAPI, requests, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
import openai
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import re
from fastapi.middleware.cors import CORSMiddleware

# from openai import OpenAI





# Helper function to process input and update the order_items dictionary
from helper.order_helper import process_order, orders, order_items, order_counter, OrderRequest, canceled_orders,   CancelOrderRequest

from helper.openaicreds import client


app = FastAPI(docs_url="/swagger", redoc_url="/redoc")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




templates = Jinja2Templates(directory="frontend_base")




@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})




# Create a new order (POST) ==> CREATING ORDERS
@app.post("/orders/", response_model=dict)
async def create_order(order_request: OrderRequest):
    global order_counter

    # Process the ordertext to update items in order items dict.
    updated_order_items = process_order(order_request.order_text)

    if updated_order_items['burger'] == 0 and updated_order_items['fries'] == 0 and updated_order_items['drink'] == 0:
        
        raise HTTPException(status_code=400, detail="Please order from available items: burger, fries, or drink.")
        
    # Add the order to the orders queue
    orders.append({"order_no": order_counter, "order_items": updated_order_items})
    
    # Generate the response with the order number
    order_response = {"order_no": order_counter, "order_items": updated_order_items}
    
    # Increment the order number for the next order
    order_counter += 1

    print(f"Order created: {order_response}")
    print("\n\n\n",orders)
    
    return order_response








# Cancel an existing order (DELETE)
@app.delete("/orders/cancel/", response_model=dict)
async def cancel_order(cancel_request: CancelOrderRequest):
    global orders, canceled_orders

    # Validate the cancel text
    if "cancel" not in cancel_request.cancel_text.lower():
        raise HTTPException(status_code=400, detail="Invalid cancellation request. Use the word 'cancel'.")

    # Find the order to cancel
    order_to_cancel = None
    for order in orders:
        if order["order_no"] == cancel_request.order_no:
            order_to_cancel = order
            break
    
    if not order_to_cancel:
        raise HTTPException(status_code=404, detail=f"Order #{cancel_request.order_no} not found.")
    
    # Remove from active orders and add to canceled orders
    orders.remove(order_to_cancel)
    canceled_orders.append(order_to_cancel)
    
    print(f"Order #{cancel_request.order_no} canceled successfully.")
    print("\n\n\n Active Orders:", orders)
    print("\n\n\n Canceled Orders:", canceled_orders)

    return {"message": f"Order #{cancel_request.order_no} canceled successfully."}




# Get all canceled orders (GET)
@app.get("/orders/canceled/", response_model=list)
async def get_canceled_orders():
    return canceled_orders




@app.get("/orders/all/", response_model=dict)
async def get_all_orders():
    # Combine active orders and canceled orders
    all_orders = {
        "active_orders": orders,
        "canceled_orders": canceled_orders
    }

    return all_orders







# API to process input through OpenAI and take actions ===> PROCESSING INPUT and calling the above APIs
@app.post("/process_input/", response_model=dict)
async def process_input(order_request: OrderRequest):
    # Call OpenAI API to process the input and determine the action

    ordered_items = order_request.order_text

    try:
        # Ensure the client is initialized correctly
        response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"User input: {ordered_items}\nPlease determine the appropriate action. Respond with either 'create_order' or 'cancel_order'. For 'create_order', return string of items and their quantities in numeric digits (example 5 burgers 4 fries 1 drink). For 'cancel_order', return 'cancel_order' and order number. If the order contains any item other than 'burger', 'fries', or 'drink', give out the reason for not being able to process the order. If the quantity is in words (e.g., 'sixteen'), convert it to digits."}
    ],
    max_tokens=50
)
        
        action = response.choices[0].message.content.strip().lower()

        print("ACTION----",action,type(action),'--->>>\n\n')
        # print("ORDER TEXT----",order_request.order_text)
        
        if "create_order" in action:
            # Extract the order items and quantities from the response
            # items = process_order(order_request.order_text)
            items = process_order(action)
            if "error" in items:
                raise HTTPException(status_code=400, detail=items["error"])
            # return await create_order(OrderRequest(order_text=order_request.order_text))
            return await create_order(OrderRequest(order_text=action))
        
        elif "cancel_order" in action:
            try:
                print("ACTION----",action,type(action))
                match = re.search(r"\d+", action)  
                order_no = match.group(0)
                print(order_no, "result")
            except:
                raise HTTPException(status_code=400, detail="Please provide a valid order number to cancel.")
            print(match, "match----")
            if match:
                print(match, "match")
                print(order_no, "order_no")
                return await cancel_order(CancelOrderRequest(order_no=order_no, cancel_text="cancel"))
            else:
                raise HTTPException(status_code=400, detail="Order number not found in the action.")
        
        else:
            raise HTTPException(status_code=400, detail="Unrecognized action.")
    
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing input {str(e)}")
   

