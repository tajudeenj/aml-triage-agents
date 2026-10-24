"""Mock AML data + tools shared by all three frameworks (Day 1-3)."""
import json

ALERTS = {
    "ALT-1001": {"customer_id": "C-501", "hit_name": "Ahmed Al Rashid", "list": "OFAC SDN",
                 "list_entry": "Ahmad Rasheed", "score": 0.87, "dob_match": False, "country_match": True,
                 "txn": {"amount": 48000, "currency": "AED", "type": "SWIFT MT103", "beneficiary_country": "TR"}},
    "ALT-1002": {"customer_id": "C-777", "hit_name": "Global Trade FZE", "list": "UN Consolidated",
                 "list_entry": "Global Trade FZE", "score": 0.99, "dob_match": None, "country_match": True,
                 "txn": {"amount": 1250000, "currency": "USD", "type": "ISO 20022 pacs.008", "beneficiary_country": "IR"}},
}
CUSTOMERS = {
    "C-501": {"name": "Ahmed Al Rashid", "dob": "1985-03-12", "nationality": "AE", "segment": "Retail",
              "risk_rating": "Low", "years_with_bank": 9, "prior_alerts_closed_fp": 4},
    "C-777": {"name": "Global Trade FZE", "nationality": "AE", "segment": "Corporate",
              "risk_rating": "High", "years_with_bank": 1, "prior_alerts_closed_fp": 0},
}
POLICY = [
    "POL-01: Score >= 0.95 with name AND country match on a sanctions list must be escalated to Compliance.",
    "POL-02: A hit may be closed as false positive if DOB does not match and customer has a clean history.",
    "POL-03: Any payment to a comprehensively sanctioned jurisdiction (IR, KP, SY, CU) must be held and escalated.",
    "POL-04: Every closure needs a written rationale referencing the policy clause used.",
]

def get_alert(alert_id: str) -> str:
    """Get sanctions screening alert details (FIRCO-style hit) by alert id, e.g. ALT-1001."""
    return json.dumps(ALERTS.get(alert_id, {"error": "alert not found"}))

def get_customer_profile(customer_id: str) -> str:
    """Get KYC customer profile and alert history by customer id, e.g. C-501."""
    return json.dumps(CUSTOMERS.get(customer_id, {"error": "customer not found"}))

def search_policy(query: str) -> str:
    """Keyword search over AML/sanctions policy clauses. (Swap for vector search/RAG later.)"""
    words = [w.lower() for w in query.split()]
    hits = [p for p in POLICY if any(w in p.lower() for w in words)]
    return "\n".join(hits or POLICY)

SCREENER = "You are the Screening Agent. Fetch the alert with get_alert and summarise the hit facts only. No decisions."
INVESTIGATOR = ("You are the Investigator Agent. Fetch the customer profile and relevant policy clauses. "
                "List evidence for true match vs false positive.")
DECISION = ("You are the Decision Agent. Recommend CLOSE_FALSE_POSITIVE or ESCALATE, cite policy clause IDs, "
            "give a 3-line rationale, then write TRIAGE_COMPLETE. Never close if a policy requires escalation.")
