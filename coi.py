import networkx as nx

# Mock wallet relationships (funding links, shared multisigs, past co-voting).
# Edit this to make your demo story.
EDGES = [
    ("0xProposer", "0xFriend"),   # funded by
    ("0xFriend", "0xGrants"),     # co-signer on the grants multisig
    ("0xProposer", "0xRandom1"),
    ("0xRandom1", "0xRandom2"),
    ("0xDelegateA", "0xRandom2"),
]

G = nx.Graph()
G.add_edges_from(EDGES)

def check_coi(proposer, recipient, max_hops=2):
    if proposer == recipient:
        return {"risk": "red", "paths": [[proposer]]}
    if proposer not in G or recipient not in G or not nx.has_path(G, proposer, recipient):
        return {"risk": "green", "paths": []}

    paths = [list(p) for p in nx.all_shortest_paths(G, proposer, recipient)]
    hops = len(paths[0]) - 1

    if hops == 1:
        risk = "red"      # direct link
    elif hops <= max_hops:
        risk = "yellow"   # one intermediary
    else:
        risk = "green"
    return {"risk": risk, "paths": paths if risk != "green" else []}

if __name__ == "__main__":
    print(check_coi("0xProposer", "0xGrants"))   # yellow
    print(check_coi("0xDelegateA", "0xGrants"))  # green