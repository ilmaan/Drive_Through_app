import openai
from openai import OpenAI
from fastapi import HTTPException
# from openaicreds import client
from helper.order_helper import *

import re


from helper.cred import key

client = openai.OpenAI(api_key=key)



async def order_using_llm(ordered_items):
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

        return action
    except Exception as e:
        print(f"Error processing input: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing input {str(e)}")

