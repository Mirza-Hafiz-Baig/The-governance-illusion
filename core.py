import hashlib, json

def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

# ---- Tamper-evident proposal history ----
def add_version(chain, text, financials, disclosures):
    prev = chain[-1]["hash"] if chain else "0" * 64
    body = {"version": len(chain) + 1, "text": text,
            "financials": financials, "disclosures": disclosures,
            "prev_hash": prev}
    body["hash"] = h(body)
    chain.append(body)
    return chain

def verify_chain(chain):
    prev = "0" * 64
    for v in chain:
        body = {k: x for k, x in v.items() if k != "hash"}
        if v["prev_hash"] != prev or h(body) != v["hash"]:
            return False, v["version"]   # tampered at this version
        prev = v["hash"]
    return True, None

# ---- Execution verifier (mocked calldata) ----
DANGER = {"upgradeTo", "delegatecall", "selfdestruct", "approve", "setOwner"}

def verify_execution(intent, actions):
    flags = []
    for a in actions:
        if a["fn"] == "transfer":
            if a["to"] != intent["recipient"] or a["amount"] != intent["amount"]:
                flags.append(f"Transfer differs from proposal: {a}")
        elif a["fn"] in DANGER:
            flags.append(f"Undisclosed {a['fn']} -> {a.get('to', '?')}")
        else:
            flags.append(f"Unknown action: {a['fn']}")
    return {"status": "red" if flags else "green", "red_flags": flags}

if __name__ == "__main__":
    intent = {"recipient": "0xGrants", "amount": 5_000_000}
    honest = [{"fn": "transfer", "to": "0xGrants", "amount": 5_000_000}]
    evil = honest + [{"fn": "upgradeTo", "to": "0xAttacker"}]
    print(verify_execution(intent, honest))   # green
    print(verify_execution(intent, evil))     # red