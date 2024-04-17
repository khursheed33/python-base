from app.llm.langchain_claude_manager import LangchainBedrockManager



bedrock_llm = LangchainBedrockManager()

res = bedrock_llm.run_conversational_chain(prompt="What is the capital of France?")

print("RES:", res)