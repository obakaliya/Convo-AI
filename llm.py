
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

load_dotenv()

model = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama3-8b-8192")

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


# Define the function that calls the model
def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": [response]}

# Define a new graph
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)
app = workflow.compile(checkpointer=MemorySaver())


def process(human_input):     
    config = {"configurable": {"thread_id": "global_thread_0011010"}}

    input_messages = [HumanMessage(human_input)]
    output = app.invoke({"messages": input_messages, "language": 'English'}, config)
    
    return output["messages"]
