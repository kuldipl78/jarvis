

# # Initialize the OpenAI client with your API key
# openai.api_key = "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"

# # Make a chat completion request
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
#         # {"role": "user", "content": "What is coding?"}
#     ]
# )

# # Print the assistant's response
# print(response["choices"][0]["message"]["content"])
