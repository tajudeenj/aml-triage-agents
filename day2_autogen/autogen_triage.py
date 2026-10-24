"""Day 2 - AutoGen (agentchat 0.7): AssistantAgent + tools, SelectorGroupChat, termination.
Run from repo root:  python -m day2_autogen.autogen_triage"""
import asyncio, os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from shared import data

async def main():
    load_dotenv()
    client = AzureOpenAIChatCompletionClient(
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        model=os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o"),
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    screener = AssistantAgent("Screener", model_client=client, tools=[data.get_alert],
                              system_message=data.SCREENER, description="Fetches and summarises the alert.")
    investigator = AssistantAgent("Investigator", model_client=client,
                                  tools=[data.get_customer_profile, data.search_policy],
                                  system_message=data.INVESTIGATOR, description="Gathers KYC and policy evidence.")
    decision = AssistantAgent("Decision", model_client=client, system_message=data.DECISION,
                              description="Makes the final close/escalate recommendation.")

    stop = TextMentionTermination("TRIAGE_COMPLETE") | MaxMessageTermination(12)
    # SelectorGroupChat: an LLM picks the next speaker. Swap in RoundRobinGroupChat to compare.
    team = SelectorGroupChat([screener, investigator, decision], model_client=client, termination_condition=stop)
    await Console(team.run_stream(task="Triage alert ALT-1002"))
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
