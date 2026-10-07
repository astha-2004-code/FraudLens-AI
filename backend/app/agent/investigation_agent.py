from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os

# Define the state graph
class AgentState(TypedDict):
    transaction_id: int
    transaction_data: Dict[str, Any]
    customer_behavior: Dict[str, Any]
    risk_score: Dict[str, Any]
    similar_cases: List[Dict[str, Any]]
    policies: List[Dict[str, Any]]
    relationships: Dict[str, Any]
    hypothesis: str
    summary: str

# Define structured output
class HypothesisOutput(BaseModel):
    hypothesis: str = Field(description="The fraud hypothesis.")
    facts: List[str] = Field(description="Facts that are 100% known.")
    inferences: List[str] = Field(description="Inferences drawn from facts.")
    unknowns: List[str] = Field(description="Information that is unknown.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

def load_transaction(state: AgentState):
    # Mock data loading for now
    state["transaction_data"] = {"id": state["transaction_id"], "amount": 100, "status": "PENDING"}
    return state

def analyze_customer(state: AgentState):
    state["customer_behavior"] = {"avg_amount": 50, "usual_country": "US"}
    return state

def calculate_risk(state: AgentState):
    state["risk_score"] = {"score": 85, "level": "CRITICAL"}
    return state

def find_similar_cases(state: AgentState):
    state["similar_cases"] = []
    return state

def find_policies(state: AgentState):
    state["policies"] = []
    return state

def analyze_relationships(state: AgentState):
    state["relationships"] = {"shared_device": False}
    return state

def generate_hypothesis(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert fraud investigator. Analyze the data and generate a hypothesis. You must distinguish between FACT, INFERENCE, and UNKNOWN. Do not invent evidence."),
        ("user", "Transaction: {transaction}\nCustomer: {customer}\nRisk: {risk}\nSimilar Cases: {similar_cases}\nPolicies: {policies}\nRelationships: {relationships}")
    ])
    
    chain = prompt | llm.with_structured_output(HypothesisOutput)
    
    # In a real scenario we pass the actual data
    try:
        res = chain.invoke({
            "transaction": state["transaction_data"],
            "customer": state["customer_behavior"],
            "risk": state["risk_score"],
            "similar_cases": state["similar_cases"],
            "policies": state["policies"],
            "relationships": state["relationships"]
        })
        state["hypothesis"] = f"FACTS: {res.facts}\nINFERENCES: {res.inferences}\nUNKNOWN: {res.unknowns}\nHYPOTHESIS: {res.hypothesis}"
    except Exception as e:
        state["hypothesis"] = "Error generating hypothesis."
    return state

def generate_summary(state: AgentState):
    state["summary"] = f"Investigation for tx {state['transaction_id']} complete. Hypothesis: {state['hypothesis']}"
    return state

def build_investigation_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("load_transaction", load_transaction)
    workflow.add_node("analyze_customer", analyze_customer)
    workflow.add_node("calculate_risk", calculate_risk)
    workflow.add_node("find_similar_cases", find_similar_cases)
    workflow.add_node("find_policies", find_policies)
    workflow.add_node("analyze_relationships", analyze_relationships)
    workflow.add_node("generate_hypothesis", generate_hypothesis)
    workflow.add_node("generate_summary", generate_summary)
    
    workflow.add_edge("load_transaction", "analyze_customer")
    workflow.add_edge("analyze_customer", "calculate_risk")
    workflow.add_edge("calculate_risk", "find_similar_cases")
    workflow.add_edge("find_similar_cases", "find_policies")
    workflow.add_edge("find_policies", "analyze_relationships")
    workflow.add_edge("analyze_relationships", "generate_hypothesis")
    workflow.add_edge("generate_hypothesis", "generate_summary")
    workflow.add_edge("generate_summary", END)
    
    workflow.set_entry_point("load_transaction")
    
    return workflow.compile()
