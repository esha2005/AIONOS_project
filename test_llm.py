from services.llm import LLMService

llm = LLMService.get_llm()

response = llm.invoke("Say hello in one sentence.")

print(response.content)