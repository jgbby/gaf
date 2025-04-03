from smolagents import CodeAgent, tool, HfApiModel, OpenAIServerModel, ToolCallingAgent
from dotenv import load_dotenv
import os
from ingest_gaf import query_contractor_profile_collection, query_reviews_collection
from typing import List
from ingest_gaf import ingest_gaf_data
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

MAX_TOKENS = 10000


# Load environment variables from a .env file
load_dotenv()

huggingface_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
reasoning_model_id = os.getenv('REASONING_MODEL_ID')
openai_api_key = os.getenv('VITE_OPENAI_API_KEY')

def get_model(model_id):
    using_huggingface = os.getenv("USE_HUGGINGFACE", "yes").lower() == "yes"
    if using_huggingface:
        return HfApiModel(model_id=model_id, token=huggingface_api_token)
    else:
        return OpenAIServerModel(
            model_id=model_id,
            api_base="http://localhost:11434/v1",
            api_key="ollama"
        )

reasoning_model = get_model('deepseek-ai/DeepSeek-R1-Distill-Qwen-32B')

@tool
def query_contractor_profile(query: str) -> tuple:
    """
    This tool queries contract profile information.
    It uses the user query to retrieve the relevant information pertaining to the contractor's profile.
    After this tool is used, immediately use reason_with_context.
    Do NOT call query_contractor_profile multiple times with the same parameter.
    Args:
        query (str): The part number extracted from the user_query.
    """
    return query_contractor_profile_collection(query)
@tool
def query_contractor_reviews(query: str) -> tuple:
    """
    This tool queries contract review information.
    It uses the user query to retrieve the relevant information pertaining to the contractor.
    After this tool is used, immediately use reason_with_context.
    Do NOT call query_contractor_reviews multiple times with the same parameter.
    Args:
        query (str): The part number extracted from the user_query.
    """
    return query_reviews_collection(query)

def compare_contractors():
    contractors = ingest_gaf_data()
    context = []
    for contractor in contractors:
        contractor_profile = query_contractor_profile(contractor)
        context.append(contractor_profile)
        
    user_query = "Compare the contractors based on their reviews and profiles. Which ones are the best?"
    prompt = f"""
    Based on the following context, compare and contrast each contractor. Be concise and specific.
    HOWEVER, do not whatsoever repeat the same tasks otherwise you will be stuck in a loop.
    Generally, at this point, you should have all the information you need to answer the user's question.
    and should not call any further tools. Your answer should not include
    any of your thinking as it will be returned to the end-user.

    Context: {context}

    Question: {user_query}

    Answer:
    """

    print(f"[compare_contractors] Prompt: {len(prompt)} tokens")
    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )
    # response = create_reasoning_agent().run(prompt, reset=False)
    return response.output_text

@tool
def reason_with_context(context: List[tuple], user_query: str) -> str:
    """
    This tool utilizes the context tuple from the query_contractor_reviews or the query_contractor_profiles 
    tool to reason about the original user inquiry and provide a concise answer. 
    This tool should be the last tool called in answering a user's prompt.
    It is important to note that this tool should not call any other tools and should only provide an answer.
    Args:
        context (List[tuple]): A list of context tuples containing the document and metadata returned from query_contractor_profile and query_contractor_reviews.
        user_query (str): The original user_query.
    """
    prompt = f"""
    Based on the following context, answer the user's question. Be concise and specific.
    If there isn't sufficient information, give as your answer a better query to perform RAG with,
    HOWEVER, do not whatsoever repeat the same tasks otherwise you will be stuck in a loop.
    Generally, at this point, you should have all the information you need to answer the user's question.
    and should not call any further tools. Your answer should be concise and not include
    any of your thinking as it will be returned to the end-user.

    Context: {context}

    Question: {user_query}

    Answer:
    """

    print(f"[reason_with_context] Prompt: {len(prompt)} tokens")

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )
    return response

def create_reasoning_agent():
    return CodeAgent(
            tools=[], 
            model=reasoning_model, 
            add_base_tools=False, 
            max_steps=2, 
            managed_agents=[],
            description="""
                You are a helpful customer agent for the company GAF, which
                consumers find roofing contractors in their areas. 
                You are NOT to respond to any inquiries outside of
                roofing contractors. Your purpose is to help the sales team of GAF with
                inquiries about contractor reviews, ratings, contact information, and geographical information.

                At this point, you should have the context you need to answer the user's question.
                You should not call any further tools. You should only answer the user's question.
                Your final answer should not include any of your thinking and should be concise and to the point. 
                """
            )

def create_tool_agent():
    return ToolCallingAgent(
            tools=[query_contractor_profile, query_contractor_reviews, reason_with_context], 
            model=reasoning_model, 
            add_base_tools=False, 
            max_steps=3, 
            managed_agents=[],
            description="""
                You are a helpful customer agent for the company GAF, which
                consumers find roofing contractors in their areas. 
                You are NOT to respond to any inquiries outside of
                roofing contractors. Your purpose is to help the sales team of GAF with
                inquiries about contractor reviews, ratings, contact information, and geographical information.

                - If a sales agent wants help rating information about the contractor 'US Roofing & Siding Inc',
                you will first call the tool query_contractor_profile with the contractor name to get the relevant information.
                query_contractor_profile() will then return a tuple of (document, metadata). This tuple is to be used
                with the reason_with_context tool to get the final answer. 
                 
                - Do NOT call query_contractor_profile multiple times with the same parameter
                - Do NOT call reason_with_context multiple times with the same context

                - Do not repeat the same queries whatsoever.
                - You are not to repeat the same queries to the user if they've already asked
                - You are to only ask the user for information that is necessary to complete the task.
                - You are to be concise and to the point. 
                """
            )

def test1():
    agent = create_tool_agent()
    # print(query_part_data("PS11752778"))
    agent.run(
        "What's the most recent review for US Roofings?"
    )