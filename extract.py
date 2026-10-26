import re, os, json

def _regex_extract(text):
    wallets = list(dict.fromkeys(re.findall(r"0x\w+", text)))

    # remove wallet addresses so their digits can't be mistaken for amounts
    clean = re.sub(r"0x\w+", " ", text)

    mult = {"million": 1_000_000, "billion": 1_000_000_000, "thousand": 1_000,
            "m": 1_000_000, "b": 1_000_000_000, "k": 1_000}
    num = r"(\d[\d,]*\.?\d*)\s*(million|billion|thousand|[MBK])?"

    # prefer a number next to a $ sign or a token name, else the first number
    m = (re.search(r"\$\s*" + num + r"\b", clean, re.I)
         or re.search(num + r"\s*(?:USDC|USDT|DAI|ETH|WETH)\b", clean, re.I)
         or re.search(num + r"\b", clean, re.I))
    amount = None
    if m:
        value = float(m.group(1).replace(",", ""))
        amount = int(value * mult.get((m.group(2) or "").lower(), 1))

    t = re.search(r"\b(USDC|USDT|DAI|ETH|WETH)\b", text, re.I)
    token = t.group(1).upper() if t else "USDC"

    # recipient: wallet in parentheses, else the one after "to"/"for"/"wallet"
    r = (re.search(r"\((0x\w+)\)", text)
         or re.search(r"\b(?:to|for|wallet)\s+(?:the\s+)?(?:\w+\s+){0,2}?(0x\w+)", text, re.I))
    recipient = r.group(1) if r else (wallets[-1] if wallets else None)

    # proposer: "proposed by 0x..", "submitted by 0x..", or a "- 0x.." signature
    p = (re.search(r"(?:proposed|submitted|posted)\s+by\s+(0x\w+)", text, re.I)
         or re.search(r"-\s*(0x\w+)\s*$", text.strip()))
    if p and p.group(1) in wallets:
        wallets.remove(p.group(1))
        wallets.insert(0, p.group(1))

    return {"amount": amount, "token": token,
            "recipient": recipient, "wallets": wallets}

def _llm_extract(text):
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    prompt = (
        "Extract from this DAO forum post. Reply with ONLY JSON, no other text, "
        'in this shape: {"amount": int, "token": str, "recipient": str, '
        '"wallets": [str]}. amount is a plain number (5M = 5000000).\n\n' + text
    )
    msg = client.messages.create(
        model="claude-sonnet-5-5", max_tokens=300,
        messages=[{"role": "user", "content": prompt}])
    raw = msg.content[0].text.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    for k in ("amount", "token", "recipient", "wallets"):
        assert k in data
    return data

def extract_claims(text):
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return _llm_extract(text)
        except Exception:
            pass  # fall back to regex
    return _regex_extract(text)

if __name__ == "__main__":
    from demo_data import FORUM_POST
    print(extract_claims(FORUM_POST))