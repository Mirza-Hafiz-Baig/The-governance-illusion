# DAO Accountability Engine

Checks whether what a DAO votes for is what its code actually does.

Built for the **Information Asymmetry** theme, Problem 1: *The Governance Illusion: DAO Accountability*.

**Team:** [team name]
**Members:** [name 1], [name 2], [name 3], [name 4]
**Demo video:** [link]

---

## The problem

In a DAO, members vote on a proposal written in plain language, but the money moves because of smart contract code. Voters rarely read that code, and the evidence they need (financial details, technical risks, who is connected to whom) is scattered across forum posts, PDFs and social media. Insiders know more than ordinary token holders, and that gap can be used against them.

A proposal can say "transfer 5M USDC to the Grants wallet" while the submitted code also hands control of a contract to an unknown address. Voters would approve the first and get the second.

## What this project does

The engine sits between the vote and the execution and runs four checks, following the evaluation chain in the problem statement:

**Proposal claims → Conflict of interest → On-chain voting → Execution discrepancy**

| Stage | What it does | Output |
|---|---|---|
| **Claims** | Reads a messy forum post and extracts the amount, token, recipient and wallet addresses | Structured claim |
| **Conflict of interest** | Finds the shortest path between the proposer's wallet and the recipient's wallet in a wallet graph | Green (no link), yellow (one intermediary), red (direct link) |
| **Vote** | Shows the result, the share of votes in favour, and the share of the treasury being spent | Passed or failed |
| **Execution** | Compares the submitted code against the approved proposal and flags any action the proposal did not mention | Green (matches) or red (mismatch, blocked) |

The final verdict is the worst result across all stages.

### Tamper-evident proposal history

Every version of a proposal is stored with a SHA-256 hash that includes the previous version's hash. If an earlier version is edited after it was recorded, its hash no longer matches and the break is shown, along with which version changed.

### Execution check

The proposal states an intent: transfer a given amount to a given recipient. The submitted code is a list of actions. Each action is compared with the intent. A transfer that differs from the proposal is flagged. Risky calls such as `upgradeTo`, `delegatecall`, `selfdestruct`, `approve` and `setOwner` are flagged when the proposal never mentioned them, and unknown actions are flagged as well.

## Demo scenarios

Use the sidebar in the dashboard.

| Setting | What you see |
|---|---|
| Default (code matches the proposal) | Conflict check is yellow because the proposer is two hops from the recipient. Verdict: **Needs review** |
| Code contains a hidden call | An extra `upgradeTo` call appears marked "not in proposal". Execution turns red. Verdict: **Execution blocked** |
| Edit version 1 after it was recorded | The first history block turns red and names the altered version. Verdict: **Execution blocked** |

## How to run

You need Python 3.9 or newer.

```bash
git clone [repo url]
cd [repo folder]
pip install -r requirements.txt
streamlit run app.py
```

On Windows, if `python` or `streamlit` is not recognised, use the `py` launcher:

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

The dashboard opens in your browser at `http://localhost:8501`.

To test a single module on its own:

```bash
python core.py       # prints one green and one red execution result
python extract.py    # prints the claims extracted from the demo forum post
python coi.py        # prints two conflict-of-interest results
```

## Project structure

```
app.py          Streamlit dashboard
core.py         Proposal hash chain and execution verifier
coi.py          Wallet graph and conflict-of-interest check
extract.py      Claim extraction from forum text
demo_data.py    Demo case: forum post, wallets, honest and malicious code, votes
.streamlit/
  config.toml   Dashboard theme
```

## What is real and what is simulated

**Working logic:**
- Claim extraction from forum text
- Shortest-path conflict-of-interest detection on a wallet graph
- The SHA-256 proposal hash chain and its verification
- The comparison of submitted actions against the approved proposal

**Simulated for the demo:**
- The blockchain. There is no deployed contract, and no real transaction is blocked.
- The wallet graph, the vote counts, the treasury size, the quorum and the dates in the audit trail. These are illustrative.
- The submitted "code". It is a simplified list of actions, not real contract bytecode.

## Design choices

- **Rule-based, not machine learning.** Every flag has a plain reason, for example "blocked because the code calls `upgradeTo`, which the proposal never mentioned". For an accountability tool, being able to explain each decision matters more than a probability score.
- **Optional LLM extraction.** `extract.py` uses pattern matching by default. If an `ANTHROPIC_API_KEY` environment variable is set and the `anthropic` package is installed, it tries a language model first and falls back to pattern matching on any failure. The demo does not need a key.

## Limitations

- Claim extraction by pattern matching handles common phrasing, not every way people write. The token defaults to USDC when the post does not name one.
- The wallet graph is mocked. A real version would build it from on-chain activity such as funding sources, shared multisigs and past voting.
- The execution check works on a decoded action list. It does not decode or simulate real bytecode, and it only catches the patterns it defines.
- Signed conflict-of-interest disclosures from proposers are not implemented.
- There is no on-chain guard. A real deployment needs a contract that refuses to execute until the checker approves.

## Next steps

1. Decode real contract calls (4-byte function selectors and arguments) instead of the simplified action list.
2. Pull real proposals and votes from a governance platform such as Snapshot.
3. Add a guard or timelock contract that only executes when the checker's attestation matches the approved proposal.
4. Require signed disclosures from proposers and use them in the conflict check.
5. Build the wallet graph from real on-chain data.

## Built with

Python, Streamlit, NetworkX, and hashlib (SHA-256).
