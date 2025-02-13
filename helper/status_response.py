# Define responses for the login endpoint
login_responses = {
    400: {
        "description": "Incorrect username or password",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Incorrect username or password"
                }
            }
        }
    }
}


# Define responses for the create_order endpoint
create_order_responses = {
    400: {
        "description": "Invalid order request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Please order from available items: burger, fries, or drink."
                }
            }
        }
    },
    200: {
        "description": "Order created successfully",
        "content": {
            "application/json": {
                "example": {
                    "order_no": 1,
                    "order_items": {
                        "burger": 2,
                        "fries": 3
                    }
                }
            }
        }
    }
}






# Define responses for the cancel_order endpoint
cancel_order_responses = {
    400: {
        "description": "Invalid cancellation request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid cancellation request. Use the word 'cancel'."
                }
            }
        }
    },
    404: {
        "description": "Order not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Order #<order_no> not found."
                }
            }
        }
    }
}