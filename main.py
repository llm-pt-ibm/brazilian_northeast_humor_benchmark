from llm_factory import LLMFactory

# Para Hugging Face local
config_hf = {
    "provider": "huggingface",
    "model_name": "mistralai/Mistral-7B-Instruct-v0.1",
    "task": "text-generation",
    "device": -1,
    "token": ''
}

# Para OpenAI API
config_openai = {
    "provider": "openai",
    "api_key": "",
    "model_name": "gpt-4"
}

llm = LLMFactory.create_llm(config_hf)
response = llm.generate("Explique o que é aprendizado de máquina.")
print(response)

llm_2 = LLMFactory.create_llm(config=config_openai)
response_2 = llm_2.generate("Explique o que é aprendizado de máquina.")
print(response_2)