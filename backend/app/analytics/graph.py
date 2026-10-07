import networkx as nx
from sqlalchemy.orm import Session
from .. import models

def build_transaction_graph(transaction: models.Transaction, db: Session):
    G = nx.Graph()
    
    # Core nodes
    G.add_node(f"Customer_{transaction.customer_id}", type="Customer", label=f"Customer {transaction.customer_id}")
    G.add_node(f"Transaction_{transaction.id}", type="Transaction", label=f"Tx {transaction.id}", amount=transaction.amount)
    G.add_edge(f"Customer_{transaction.customer_id}", f"Transaction_{transaction.id}")
    
    # Device node
    if transaction.device_id:
        G.add_node(f"Device_{transaction.device_id}", type="Device", label=f"Device {transaction.device_id}")
        G.add_edge(f"Customer_{transaction.customer_id}", f"Device_{transaction.device_id}")
        G.add_edge(f"Transaction_{transaction.id}", f"Device_{transaction.device_id}")
        
        # Check for other customers using this device
        shared_devices = db.query(models.Transaction).filter(
            models.Transaction.device_id == transaction.device_id,
            models.Transaction.customer_id != transaction.customer_id
        ).limit(10).all()
        
        for sd in shared_devices:
            G.add_node(f"Customer_{sd.customer_id}", type="Customer", label=f"Customer {sd.customer_id}")
            G.add_edge(f"Customer_{sd.customer_id}", f"Device_{transaction.device_id}")
            
    # Merchant node
    if transaction.merchant_id:
        G.add_node(f"Merchant_{transaction.merchant_id}", type="Merchant", label=f"Merchant {transaction.merchant_id}")
        G.add_edge(f"Customer_{transaction.customer_id}", f"Merchant_{transaction.merchant_id}")
        G.add_edge(f"Transaction_{transaction.id}", f"Merchant_{transaction.merchant_id}")
        
    # IP Address node
    if transaction.ip_address:
        G.add_node(f"IP_{transaction.ip_address}", type="IP", label=f"IP {transaction.ip_address}")
        G.add_edge(f"Customer_{transaction.customer_id}", f"IP_{transaction.ip_address}")
        G.add_edge(f"Transaction_{transaction.id}", f"IP_{transaction.ip_address}")
        
    # Convert to format suitable for frontend visualization
    nodes = [{"id": n, **G.nodes[n]} for n in G.nodes()]
    edges = [{"source": u, "target": v} for u, v in G.edges()]
    
    return {"nodes": nodes, "edges": edges}
