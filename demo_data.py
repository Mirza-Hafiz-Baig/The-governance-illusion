FORUM_POST = """Hey all, proposing a $5M treasury grant to the Grants Wallet (0xGrants)
to fund ecosystem work. Details in the linked PDF. - 0xProposer"""

PROPOSER = "0xProposer"
RECIPIENT = "0xGrants"
INTENT = {"recipient": "0xGrants", "amount": 5_000_000}

ACTIONS_HONEST = [{"fn": "transfer", "to": "0xGrants", "amount": 5_000_000}]
ACTIONS_EVIL = ACTIONS_HONEST + [{"fn": "upgradeTo", "to": "0xAttacker"}]

VOTES = {"for": 6200, "against": 1800}