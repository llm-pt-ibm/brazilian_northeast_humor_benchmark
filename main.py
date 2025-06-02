from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
    model="o3-mini",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Explique a teoria da relatividade de forma simples."}
    ],
    max_completion_tokens=600
)

print(response.choices[0].message.content)