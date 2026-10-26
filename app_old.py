import streamlit as st
from demo_data import *

from extract import extract_claims as get_claims
from coi import check_coi as get_coi
from core import verify_execution as get_exec

ICON = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

st.title("DAO Accountability Engine")
scenario = st.radio("Proposal submitted to chain:",
                    ["Honest bytecode", "Malicious bytecode"], horizontal=True)
actions = ACTIONS_HONEST if scenario == "Honest bytecode" else ACTIONS_EVIL

st.subheader("Forum post")
st.code(FORUM_POST)

claims = get_claims(FORUM_POST)
coi = get_coi(PROPOSER, RECIPIENT)
votes_pass = VOTES["for"] > VOTES["against"]
ex = get_exec(INTENT, actions)

c1, c2, c3, c4 = st.columns(4)
c1.metric("1. Claims", f"{ICON['green']} ok")
c2.metric("2. Conflict of interest", f"{ICON[coi['risk']]} {coi['risk']}")
c3.metric("3. Vote", f"{ICON['green']} passed" if votes_pass else f"{ICON['red']} failed")
c4.metric("4. Execution", f"{ICON[ex['status']]} {ex['status']}")

st.subheader("Extracted claims")
st.json(claims)

st.subheader("Conflict-of-interest path")
for p in coi["paths"]:
    st.write(" → ".join(p))

st.subheader("Execution check")
if ex["status"] == "red":
    st.error("EXECUTION HALTED: code does not match what the community voted for")
    for f in ex["red_flags"]:
        st.write("•", f)
else:
    st.success("Code matches the approved proposal. Safe to execute.")


from core import add_version, verify_chain

st.subheader("Proposal history (tamper-evident)")
chain = []
add_version(chain, "Grant 5M to Grants Wallet", INTENT, ["none"])
add_version(chain, "Grant 5M to Grants Wallet (clarified)", INTENT, ["friend of recipient"])
if st.checkbox("Simulate tampering with version 1"):
    chain[0]["text"] = "Grant 50M to Grants Wallet"
ok, bad = verify_chain(chain)
if ok:
    st.success("Chain intact")
else:
    st.error(f"Tampered at version {bad}")
for v in chain:
    st.code(f"v{v['version']}  hash: {v['hash'][:16]}...  prev: {v['prev_hash'][:16]}...")


score = {"green": 0, "yellow": 0.5, "red": 1}
worst = max(score[coi["risk"]], score[ex["status"]], 0 if ok else 1)
verdict = "🔴 BLOCK" if worst == 1 else "🟡 REVIEW" if worst == 0.5 else "🟢 SAFE"
st.header(f"Final verdict: {verdict}")
