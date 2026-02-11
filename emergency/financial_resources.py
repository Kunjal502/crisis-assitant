FINANCIAL_SUPPORT = {
    "india": [
        "https://www.nabard.org",
        "https://www.mygov.in",
        "Local district financial counseling centers"
    ]
}

EMERGENCY_CONTACTS = {
    "police": {
        "india": "100",
        "general": "Emergency: 100 (India) / 911 (US)"
    },
    "ambulance": {
        "india": "102",
        "general": "Emergency: 102 (India) / 911 (US)"
    },
    "financial_helpline": {
        "india": "National Financial Literacy Helpline: 155255",
        "general": "Contact your local financial counseling center"
    },
    "consumer_helpline": {
        "india": "National Consumer Helpline: 1800-11-4000",
        "general": "Consumer complaints: Check local helpline"
    }
}

def get_resources(region="india"):
    return FINANCIAL_SUPPORT.get(region, [])

def get_emergency_contacts(situation_text: str, region="india"):
    """Get emergency contacts only when truly needed (police/ambulance/consumer)."""
    contacts = {}
    
    situation_lower = situation_text.lower()

    vehicle_terms = ["car", "vehicle", "bike", "scooter", "motorcycle"]
    theft_terms = ["stolen", "theft", "robbery", "fraud", "scam", "cheated"]
    lost_terms = ["lost", "missing"]

    # Police-related: theft/robbery/fraud or lost vehicle
    if any(term in situation_lower for term in theft_terms) or (
        any(v in situation_lower for v in vehicle_terms) and any(l in situation_lower for l in lost_terms)
    ):
        contacts["Police"] = EMERGENCY_CONTACTS["police"].get(region, EMERGENCY_CONTACTS["police"]["general"])
    
    # Medical emergency
    if any(word in situation_lower for word in ["medical", "hospital", "health", "accident", "injury", "emergency"]):
        contacts["Ambulance"] = EMERGENCY_CONTACTS["ambulance"].get(region, EMERGENCY_CONTACTS["ambulance"]["general"])
    
    # Consumer issues (fraud/scam)
    if any(word in situation_lower for word in ["fraud", "scam", "cheated", "consumer"]):
        contacts["Consumer Helpline"] = EMERGENCY_CONTACTS["consumer_helpline"].get(region, EMERGENCY_CONTACTS["consumer_helpline"]["general"])
    
    return contacts
