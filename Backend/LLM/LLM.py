import os
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import sys
from openai import OpenAI

# print("Current Working Directory:", os.getcwd())
if __name__ == "__main__":
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("Output.txt", "w", encoding="utf-8")
    sys.stderr = open("Error.txt", "w")

    # Read all questions from input.txt
    questions = [line.strip() for line in sys.stdin if line.strip()]

    # Initialize OpenRouter client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="Enter your api key here"  # Set this env variable OR hardcode your key
    )

    # Call the API for each question
    for i, question in enumerate(questions, 1):
        try:
            completion = client.chat.completions.create(
                model="qwen/qwen-2.5-72b-instruct:free",
                messages=[{"role": "user", "content": question}],
                extra_headers={
                    "HTTP-Referer": "https://your-site.com",  # Optional
                    "X-Title": "Your Site Name"               # Optional
                }
            )

            print(f"\n--- Question {i} ---")
            print(f"Q: {question}")
            print(f"A: {completion.choices[0].message.content.strip()}")
        
        except Exception as e:
            print(f"Error processing Question {i}: {question}")
            print(str(e))



    
