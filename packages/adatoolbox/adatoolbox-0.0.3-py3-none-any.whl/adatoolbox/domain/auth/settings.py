import os

API_AD_URL =  os.getenv("API_AD_URL")

assert API_AD_URL, "Environment variable API_AD_URL not found"
