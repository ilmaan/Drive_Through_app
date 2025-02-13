from fastapi import FastAPI, requests, Request, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
import openai
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import re
from fastapi.middleware.cors import CORSMiddleware

# Helper function to process input and update the order_items dictionary
from helper.order_helper import process_order, orders, order_items, order_counter, OrderRequest, canceled_orders,   CancelOrderRequest
from helper.llm_processing import order_using_llm
from helper.auth import test_user, verify_password, create_access_token, OAuth2PasswordRequestForm
from helper.status_response import login_responses, create_order_responses, cancel_order_responses


app = FastAPI(docs_url="/swagger", redoc_url="/redoc")




# ADDED MIDDLEWARES __ MESSED CODE FROM FRONTEND ALLOWANCE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




templates = Jinja2Templates(directory="html_templates")




@app.get("/", response_class=HTMLResponse, summary="Home Page", description="Returns the home page for the API.")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})







@app.post("/orders/", response_model=dict, responses=create_order_responses, summary="Create Order", description="Create a new order with specified items.")
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
@app.delete("/orders/cancel/", response_model=dict, responses=cancel_order_responses, summary="Cancel Order", description="Cancel an existing order by order number.")
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
@app.get("/orders/canceled/", response_model=list, summary="Get Canceled Orders", description="Retrieve a list of all canceled orders.")
async def get_canceled_orders():
    return canceled_orders




@app.get("/orders/all/", response_model=dict, summary="Get All Orders", description="Retrieve all active and canceled orders.")
async def get_all_orders():
    # Combine active orders and canceled orders
    print("****"*10)
    all_orders = {
        "active_orders": orders,
        "canceled_orders": canceled_orders
    }

    return all_orders




# API to process input through OpenAI and take actions ===> PROCESSING INPUT and calling the above APIs
@app.post("/process_input/", response_model=dict, responses={400: {"description": "Error processing input", "content": {"application/json": {"example": {"detail": "Error processing input <error_message>"}}}}}, summary="Process Input", description="Process input through OpenAI and take actions based on the response.")
async def process_input(order_request: OrderRequest):
   
    ordered_items = order_request.order_text

    try:
        # ADDED OPEN AI CALL IN HELPER FUNCTIONS
        action = await order_using_llm(ordered_items)

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
   


# Login endpoint for authentication Note --- API cannot be hit withiout authentication
# @app.post("/token", response_model=dict, responses=login_responses, summary="User Login", description="Authenticate a user and return an access token.")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = test_user.get(form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


