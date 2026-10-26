import streamlit as st
from demo_data import *
from extract import extract_claims as get_claims
from coi import check_coi as get_coi
from core import verify_execution as get_exec, add_version, verify_chain

st.set_page_config(page_title="DAO Accountability Engine", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&family=Source+Serif+4:wght@600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"], .stMarkdown p { font-family: 'Public Sans', sans-serif; font-size: 17px; color: #0F2237; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1300px !important; padding: 0 3rem 3rem 3rem !important; }
h1, h2, h3 { font-family: 'Source Serif 4', serif !important; color: #0F2237; letter-spacing: -0.01em; }
h3 { font-size: 1.6rem !important; margin-top: 1.6rem; }
[data-testid="stSidebar"] { background: #0F2237; }
[data-testid="stSidebar"] * { color: #E6ECF3 !important; }

.masthead { background: #0F2237; padding: 30px 36px; margin: 1.5rem 0 1.4rem 0; display: flex; justify-content: space-between; align-items: flex-end; }
.masthead .name { font-family: 'Source Serif 4', serif; font-size: 2.6rem; font-weight: 700; color: #FFFFFF; line-height: 1.1; }
.masthead .sub { color: #B9C6D6; margin-top: 8px; font-size: 1.05rem; }
.masthead .prop { text-align: right; color: #B9C6D6; font-size: 1rem; }
.masthead .prop b { display: block; color: #FFFFFF; font-size: 1.15rem; font-weight: 600; }
.quote { border-left: 4px solid #2B4C7E; padding: 6px 0 6px 18px; font-size: 1.1rem; color: #2A3A4D; margin-bottom: 1.6rem; white-space: pre-line; }

.trail { display: flex; background: #fff; border: 1px solid #D3D9E1; margin-bottom: 1.6rem; }
.step { flex: 1; padding: 22px 26px; position: relative; border-right: 1px solid #D3D9E1; }
.step:last-child { border-right: none; }
.step:not(:last-child)::after { content: ""; position: absolute; right: -9px; top: 33px; width: 16px; height: 16px; background: #fff; border-top: 1px solid #D3D9E1; border-right: 1px solid #D3D9E1; transform: rotate(45deg); z-index: 2; }
.node { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; margin-bottom: 14px; }
.step-name { font-size: 0.95rem; color: #5B6B7D; }
.step-word { font-size: 1.65rem; font-weight: 600; margin: 2px 0 4px 0; }
.step-detail { font-size: 0.95rem; color: #5B6B7D; }

.verdict { display: flex; justify-content: space-between; align-items: center; padding: 30px 36px; border: 1px solid; border-left-width: 8px; margin-bottom: 1.8rem; }
.verdict h2 { margin: 0 0 8px 0; font-size: 2.6rem !important; }
.verdict p { margin: 3px 0; font-size: 1.15rem; }
.pill { color: #fff; padding: 8px 20px; font-weight: 600; font-size: 1.05rem; white-space: nowrap; }

.diff { background: #fff; border: 1px solid #D3D9E1; }
.diff-head { padding: 12px 18px; border-bottom: 1px solid #D3D9E1; font-weight: 600; background: #F7F9FB; }
.line { display: flex; align-items: center; font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 0.95rem; padding: 12px 0; border-bottom: 1px solid #EEF1F5; }
.gutter { width: 44px; text-align: center; color: #8A97A6; flex-shrink: 0; }
.code { flex: 1; }
.line.bad { background: #FDECEA; color: #8F1F17; font-weight: 500; }
.line.bad .gutter { color: #C0352B; font-weight: 700; }
.tag { margin-right: 14px; font-family: 'Public Sans', sans-serif; font-size: 0.8rem; background: #C0352B; color: #fff; padding: 3px 10px; white-space: nowrap; }

.panel { background: #fff; border: 1px solid #D3D9E1; padding: 22px 26px; min-height: 340px; }
.panel-title { font-weight: 600; font-size: 1.1rem; margin-bottom: 14px; }
.sum { margin: 0 0 14px 0 !important; line-height: 1.5; }
.ref { margin-left: 8px; font-size: 0.8rem; color: #2B4C7E; border: 1px solid #C5D1E0; padding: 1px 8px; white-space: nowrap; }
.bigrow { font-size: 1rem; color: #5B6B7D; margin-bottom: 8px; }
.big { font-family: 'Source Serif 4', serif; font-size: 2.4rem; font-weight: 700; color: #0F2237; margin-right: 6px; }
.bar { display: flex; height: 14px; background: #E3E8EE; margin-bottom: 8px; }
.bar div { height: 100%; }
.meta { font-size: 0.95rem; color: #5B6B7D; margin-top: 4px; }

.ev { display: flex; align-items: flex-start; padding: 11px 0; border-bottom: 1px solid #EEF1F5; }
.ev .when { width: 70px; color: #5B6B7D; font-size: 0.95rem; flex-shrink: 0; }
.ev .dot { width: 11px; height: 11px; border-radius: 50%; margin: 6px 14px 0 0; flex-shrink: 0; }
.rb { display: flex; align-items: center; margin: 14px 0; }
.rb .lab { width: 170px; flex-shrink: 0; }
.rb .track { flex: 1; height: 14px; background: #E3E8EE; }
.rb .fill { height: 100%; }
.rb .num { width: 54px; text-align: right; font-weight: 600; }

.chain { display: flex; align-items: stretch; }
.block { flex: 1; background: #fff; border: 1px solid #D3D9E1; padding: 18px 22px; }
.block.bad { border-color: #C0352B; background: #FDECEA; }
.block .title { font-weight: 600; margin-bottom: 8px; }
.block .k { color: #5B6B7D; font-size: 0.85rem; margin-top: 6px; }
.block .v { font-family: 'IBM Plex Mono', Consolas, monospace; font-size: 0.95rem; }
.block .warn { color: #C0352B; font-weight: 600; margin-top: 8px; }
.link { width: 44px; display: flex; align-items: center; justify-content: center; color: #8A97A6; font-size: 1.5rem; }
.foot { color: #5B6B7D; font-size: 0.9rem; margin-top: 2.4rem; border-top: 1px solid #D3D9E1; padding-top: 14px; }
</style>
""", unsafe_allow_html=True)

COL = {"green": "#1E7B55", "yellow": "#B7791F", "red": "#C0352B"}
TINT = {"green": "#E7F4EC", "yellow": "#FEF6E3", "red": "#FDECEA"}
RANK = {"green": 0, "yellow": 1, "red": 2}
SC = {"green": 0, "yellow": 50, "red": 100}
GLYPH = {"green": "✓", "yellow": "!", "red": "✕"}

# Mock DAO facts (say "illustrative" in the README)
TREASURY = 42_000_000
QUORUM = 5_000

# ---------- sidebar ----------
with st.sidebar:
    st.subheader("Demo controls")
    scenario = st.radio("Code submitted on-chain",
                        ["Matches the proposal", "Contains a hidden call"])
    tamper = st.checkbox("Edit version 1 after it was recorded")

actions = ACTIONS_HONEST if scenario == "Matches the proposal" else ACTIONS_EVIL

# ---------- pipeline ----------
claims = get_claims(FORUM_POST)
coi = get_coi(PROPOSER, RECIPIENT)
ex = get_exec(INTENT, actions)
vote_pass = VOTES["for"] > VOTES["against"]
total_votes = VOTES["for"] + VOTES["against"]
pct_for = VOTES["for"] / total_votes * 100
amount = claims["amount"] or 0
share = amount / TREASURY * 100

chain = []
add_version(chain, "Grant 5M to Grants Wallet", INTENT, ["none"])
add_version(chain, "Grant 5M to Grants Wallet (clarified)", INTENT, ["friend of recipient"])
if tamper:
    chain[0]["text"] = "Grant 50M to Grants Wallet"
chain_ok, bad_v = verify_chain(chain)

hops = len(coi["paths"][0]) - 1 if coi["paths"] else None
coi_word = {"green": "Clear", "yellow": "Linked", "red": "Direct link"}[coi["risk"]]

# ---------- masthead ----------
st.markdown(
    '<div class="masthead"><div>'
    '<div class="name">DAO Accountability Engine</div>'
    '<div class="sub">Checks whether what a DAO votes for is what its code actually does.</div></div>'
    '<div class="prop"><b>Proposal #142</b>Ecosystem Grants Round 3</div></div>',
    unsafe_allow_html=True)
st.markdown(f'<div class="quote">{FORUM_POST}</div>', unsafe_allow_html=True)

# ---------- decision trail ----------
def step(name, status, word, detail):
    return (f'<div class="step"><div class="node" style="background:{COL[status]}">{GLYPH[status]}</div>'
            f'<div class="step-name">{name}</div>'
            f'<div class="step-word" style="color:{COL[status]}">{word}</div>'
            f'<div class="step-detail">{detail}</div></div>')

coi_detail = f"{hops} hops apart" if hops else "No connection found"
trail = "".join([
    step("Claims", "green", "Extracted", f'{amount:,} {claims["token"]} to {claims["recipient"]}'),
    step("Conflict of interest", coi["risk"], coi_word, coi_detail),
    step("Vote", "green" if vote_pass else "red", "Passed" if vote_pass else "Failed",
         f'{VOTES["for"]:,} for, {VOTES["against"]:,} against'),
    step("Execution", ex["status"], "Matches" if ex["status"] == "green" else "Mismatch",
         "Code equals proposal" if ex["status"] == "green" else f'{len(ex["red_flags"])} unexpected call(s)'),
])
st.markdown(f'<div class="trail">{trail}</div>', unsafe_allow_html=True)

# ---------- verdict ----------
level = max(RANK[coi["risk"]], RANK[ex["status"]], 0 if chain_ok else 2)
status = ["green", "yellow", "red"][level]
title = {"green": "Safe to execute", "yellow": "Needs review", "red": "Execution blocked"}[status]
risk_label = {"green": "Low risk", "yellow": "Moderate risk", "red": "High risk"}[status]

reasons = []
if ex["status"] == "red":
    reasons.append("The submitted code does something the proposal never mentions.")
if hops:
    reasons.append(f"The proposer is {hops} hops from the recipient wallet.")
if not chain_ok:
    reasons.append(f"The proposal text changed after version {bad_v} was recorded.")
if not reasons:
    reasons.append("The code matches the proposal and no conflicts were found.")
body = "".join(f"<p>{r}</p>" for r in reasons)

st.markdown(
    f'<div class="verdict" style="background:{TINT[status]};border-color:{COL[status]}">'
    f'<div><h2 style="color:{COL[status]}">{title}</h2>{body}</div>'
    f'<div class="pill" style="background:{COL[status]}">{risk_label}</div></div>',
    unsafe_allow_html=True)

# ---------- proposal against code ----------
st.subheader("Proposal against code")

def show(a):
    if a["fn"] == "transfer":
        return f'transfer(to={a["to"]}, amount={a["amount"]:,})'
    return f'{a["fn"]}({a.get("to", "")})'

def expected(a):
    return (a["fn"] == "transfer" and a["to"] == INTENT["recipient"]
            and a["amount"] == INTENT["amount"])

def line(n, text, bad=False):
    cls = "line bad" if bad else "line"
    gut = "!" if bad else str(n)
    tag = '<span class="tag">not in proposal</span>' if bad else ""
    return f'<div class="{cls}"><span class="gutter">{gut}</span><span class="code">{text}</span>{tag}</div>'

approved = {"fn": "transfer", "to": INTENT["recipient"], "amount": INTENT["amount"]}
left_html = '<div class="diff"><div class="diff-head">Approved proposal</div>' + line(1, show(approved)) + '</div>'
right_rows = "".join(line(i + 1, show(a), bad=not expected(a)) for i, a in enumerate(actions))
right_html = '<div class="diff"><div class="diff-head">Submitted code</div>' + right_rows + '</div>'
d1, d2 = st.columns(2)
d1.markdown(left_html, unsafe_allow_html=True)
d2.markdown(right_html, unsafe_allow_html=True)

# ---------- summary, vote, map ----------
st.subheader("Decision summary")

items = [("Claims", f'Requests {amount:,} {claims["token"]} for {claims["recipient"]}, {share:.1f}% of the treasury.')]
if hops and hops > 1:
    items.append(("Conflict map", f"The proposer reaches the recipient through {hops - 1} intermediary wallet(s)."))
elif hops:
    items.append(("Conflict map", "The proposer is directly linked to the recipient."))
else:
    items.append(("Conflict map", "No link between proposer and recipient was found."))
if vote_pass:
    quorum_text = "above" if total_votes >= QUORUM else "below"
    items.append(("Vote", f"Passed with {pct_for:.0f}% in favour, {quorum_text} the quorum of {QUORUM:,} votes."))
else:
    items.append(("Vote", "Did not pass."))
if ex["status"] == "green":
    items.append(("Execution", "The submitted code matches the approved proposal."))
else:
    items.append(("Execution", f'{len(ex["red_flags"])} call(s) not in the proposal: {ex["red_flags"][0]}'))

summary_html = ('<div class="panel"><div class="panel-title">What the evidence shows</div>'
                + "".join(f'<p class="sum">{t}<span class="ref">{r}</span></p>' for r, t in items)
                + '</div>')

quorum_met = "met" if total_votes >= QUORUM else "not met"
vote_html = (
    '<div class="panel"><div class="panel-title">Vote</div>'
    f'<div class="bigrow"><span class="big">{pct_for:.0f}%</span>in favour</div>'
    f'<div class="bar"><div style="width:{pct_for:.1f}%;background:#1E7B55"></div>'
    f'<div style="width:{100 - pct_for:.1f}%;background:#C0352B"></div></div>'
    f'<div class="meta">{VOTES["for"]:,} for, {VOTES["against"]:,} against</div>'
    f'<div class="meta">Quorum of {QUORUM:,} votes: {quorum_met}</div>'
    '<div class="panel-title" style="margin-top:24px">Treasury impact</div>'
    f'<div class="bigrow"><span class="big">{share:.1f}%</span>of treasury</div>'
    f'<div class="bar"><div style="width:{min(share, 100):.1f}%;background:#2B4C7E"></div></div>'
    f'<div class="meta">{amount:,} of {TREASURY:,} {claims["token"]}</div></div>')

def short(w):
    return w if len(w) <= 12 else w[:6] + "…" + w[-4:]

def coi_svg(path, color):
    n = len(path)
    xs = [70 + i * (380 / max(n - 1, 1)) for i in range(n)]
    parts = []
    for i in range(n - 1):
        parts.append(f'<line x1="{xs[i]:.0f}" y1="80" x2="{xs[i + 1]:.0f}" y2="80" stroke="{color}" stroke-width="2.5" stroke-dasharray="7 6"/>')
    for i, w in enumerate(path):
        role = "Proposer" if i == 0 else ("Recipient" if i == n - 1 else "Intermediary")
        fill = color if i in (0, n - 1) else "#FFFFFF"
        parts.append(f'<circle cx="{xs[i]:.0f}" cy="80" r="16" fill="{fill}" stroke="{color}" stroke-width="2.5"/>')
        parts.append(f'<text x="{xs[i]:.0f}" y="45" text-anchor="middle" font-size="13" fill="#5B6B7D">{role}</text>')
        parts.append(f'<text x="{xs[i]:.0f}" y="125" text-anchor="middle" font-size="12" font-family="monospace" fill="#0F2237">{short(w)}</text>')
    return '<svg viewBox="0 0 520 150" width="100%">' + "".join(parts) + '</svg>'

path = coi["paths"][0] if coi["paths"] else [PROPOSER, RECIPIENT]
map_color = COL[coi["risk"]] if coi["paths"] else "#8A97A6"
caption = f"{hops} hops between proposer and recipient." if hops else "No path found between these wallets."
map_html = ('<div class="panel"><div class="panel-title">Conflict-of-interest map</div>'
            + coi_svg(path, map_color) + f'<div class="meta">{caption}</div></div>')

s1, s2, s3 = st.columns([1.2, 1, 1.2])
s1.markdown(summary_html, unsafe_allow_html=True)
s2.markdown(vote_html, unsafe_allow_html=True)
s3.markdown(map_html, unsafe_allow_html=True)

# ---------- event log and risk breakdown ----------
st.subheader("Audit trail")
events = [
    ("Day 1", "Forum post published", "green"),
    ("Day 1", f'Claims extracted: {amount:,} {claims["token"]}', "green"),
    ("Day 1", f"Conflict check: {coi_word.lower()}", coi["risk"]),
    ("Day 4", "Vote closed: " + ("passed" if vote_pass else "failed"), "green" if vote_pass else "red"),
    ("Day 5", "Code submitted on-chain", "green"),
    ("Day 5", "Guard checked the code: " + ("matches" if ex["status"] == "green" else "mismatch, execution halted"), ex["status"]),
]
ev_html = '<div class="panel"><div class="panel-title">Event log</div>' + "".join(
    f'<div class="ev"><span class="when">{w}</span><span class="dot" style="background:{COL[s]}"></span><span>{t}</span></div>'
    for w, t, s in events) + '</div>'

risk_rows = [
    ("Claims", 0, "green"),
    ("Conflict of interest", SC[coi["risk"]], coi["risk"]),
    ("Vote", 0 if vote_pass else 100, "green" if vote_pass else "red"),
    ("Execution", SC[ex["status"]], ex["status"]),
    ("Proposal history", 0 if chain_ok else 100, "green" if chain_ok else "red"),
]
rb_html = '<div class="panel"><div class="panel-title">Risk by stage (0 safe, 100 critical)</div>' + "".join(
    f'<div class="rb"><span class="lab">{n}</span><div class="track"><div class="fill" style="width:{sc}%;background:{COL[s]}"></div></div>'
    f'<span class="num" style="color:{COL[s]}">{sc}</span></div>'
    for n, sc, s in risk_rows) + '</div>'

a1, a2 = st.columns(2)
a1.markdown(ev_html, unsafe_allow_html=True)
a2.markdown(rb_html, unsafe_allow_html=True)

with st.expander("Extracted claims (raw)"):
    st.json(claims)

# ---------- hash history ----------
st.subheader("Proposal history")
blocks = []
for v in chain:
    bad = (not chain_ok) and v["version"] == bad_v
    warn = '<div class="warn">Edited after it was recorded</div>' if bad else ""
    blocks.append(
        f'<div class="block{" bad" if bad else ""}"><div class="title">Version {v["version"]}</div>'
        f'<div class="k">Hash</div><div class="v">{v["hash"][:16]}</div>'
        f'<div class="k">Follows</div><div class="v">{v["prev_hash"][:16]}</div>{warn}</div>')
st.markdown('<div class="chain">' + '<div class="link">→</div>'.join(blocks) + '</div>',
            unsafe_allow_html=True)

st.markdown('<div class="foot">Simulated chain with rule-based checks. Treasury size, quorum and event timings are illustrative. Claim extraction uses pattern matching, and no model is trained.</div>',
            unsafe_allow_html=True)