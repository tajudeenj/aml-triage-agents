"""Day 3 - Microsoft Agent Framework 1.x (successor to SK + AutoGen): Agent, tools, Sequential orchestration.
Run from repo root:  python -m day3_agent_framework.maf_triage"""
import asyncio, os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient
from agent_framework.orchestrations import SequentialBuilder
from shared import data

async def main():
    load_dotenv()
    client = OpenAIChatCompletionClient(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    screener = Agent(client, data.SCREENER, name="Screener", tools=[data.get_alert])
    investigator = Agent(client, data.INVESTIGATOR, name="Investigator",
                         tools=[data.get_customer_profile, data.search_policy])
    decision = Agent(client, data.DECISION, name="Decision")

    # 1) Single agent run
    r = await screener.run("Summarise alert ALT-1001")
    print("== Single agent ==\n", r.text)

    # 2) Multi-agent workflow: Screener -> Investigator -> Decision (shared conversation)
    workflow = SequentialBuilder(participants=[screener, investigator, decision]).build()
    result = await workflow.run("Triage alert ALT-1002")
    print("\n== Sequential workflow ==")
    for output in result.get_outputs():
        for msg in (output if isinstance(output, list) else [output]):
            print(f"[{getattr(msg, 'author_name', '') or getattr(msg, 'role', '')}] {getattr(msg, 'text', msg)}\n")

if __name__ == "__main__":
    asyncio.run(main())
