import openai
from openai import OpenAI
from helper.cred import key

client = openai.OpenAI(api_key=key)
