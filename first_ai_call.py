import ollama

print("Sending question to local AI...")
print("-" * 40)

response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {
            'role': 'user',
            'content': 'In one paragraph, what is JCL and why is it important?'
        }
    ]
)

print(response['message']['content'])
print("-" * 40)
print("Done! That response came from your local Mac - zero internet used.")