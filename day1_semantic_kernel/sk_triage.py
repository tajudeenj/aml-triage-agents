"""Day 1 - Semantic Kernel: plugins (kernel_function), auto function calling, ChatCompletionAgent.
Run from repo root:  python -m day1_semantic_kernel.sk_triage"""
import asyncio
from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from shared import data

class AmlPlugin:
    """A plugin = a class of native functions the LLM can call."""
    @kernel_function(description="Get sanctions screening alert details by alert id")
    def get_alert(self, alert_id: str) -> str: return data.get_alert(alert_id)

    @kernel_function(description="Get KYC customer profile by customer id")
    def get_customer_profile(self, customer_id: str) -> str: return data.get_customer_profile(customer_id)

    @kernel_function(description="Search AML policy clauses by keywords")
    def search_policy(self, query: str) -> str: return data.search_policy(query)

async def main():
    load_dotenv()
    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),          # reads AZURE_OPENAI_* from .env
        name="AmlTriage",
        instructions=data.SCREENER + " Then " + data.INVESTIGATOR + " Then " + data.DECISION,
        plugins=[AmlPlugin()],                  # function calling = Auto when plugins are given
    )
    for alert in ["ALT-1001", "ALT-1002"]:
        resp = await agent.get_response(messages=f"Triage alert {alert}")
        print(f"\n===== {alert} =====\n{resp.content}")

if __name__ == "__main__":
    asyncio.run(main())
