from openai import OpenAI
import os
client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY") 
    )  

def lastWordWas():
    with open("lastWord.txt", "r") as file_object:
        content = file_object.read()
        #print(content)
        return content
    

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": f"""
        You are AI assistant.Your work is give me a random english word everyday with bangla meaning and also 2 examples.
        The difficulty level of the words are will go to beginner to hard and expert day by day. Your last word was {lastWordWas()} .
        Give me the word of today.
        
        Note : I need only the last given word on top line. Then you response.
     
     """}
  ]
)

respons = completion.choices[0].message.content
word=""
for i in respons:
    if i=='\n':
        break
    word+=i
# print(word)
print(respons)
with open("lastWord.txt", "a",encoding="utf-8") as file_object:
    content = file_object.writelines(word)
    # print(content)
