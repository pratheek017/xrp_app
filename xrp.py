# App to create a wallet with 10k XRP on the testnet and send some XRP to a dummy account

# I. Perform a transaction (send some XRP from an account)

# Step 1
# Define the network client
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/" # testnet url
# JSON_RPC_URL = "https://s2.ripple.com:51234/" # mainnet url

from xrpl.clients import JsonRpcClient
client = JsonRpcClient(JSON_RPC_URL)

print(f'Testnet client setup')

# Step 2
# Create a wallet using the testnet faucet (gets funded with 10k XRP)
# https://xrpl.org/xrp-testnet-faucet.html
from xrpl.wallet import generate_faucet_wallet
test_wallet = generate_faucet_wallet(client, debug=True)

print(f'Test wallet - {test_wallet}')

test_account = test_wallet.address

# Step 3
# Retrieving the wallet balance and printing
from xrpl.models.requests import AccountInfo
account_info = AccountInfo(
    account=test_account,
    ledger_index="validated",
    strict=True
)

account_info_response = client.request(account_info)
account_balance_raw = account_info_response.result["account_data"]["Balance"]
account_balance = int(account_balance_raw) / 1000000

print(f'Account balance: {account_balance} XRP')

# Step 4
# Preparing a transaction to send some XRP to another account
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops

# Transaction to send 30 XRP to the mentioned wallet address
xrp_to_send = 40
my_payment_tx = Payment(
    account=test_account,
    amount=xrp_to_drops(xrp_to_send),
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe"
)

# Step 5
# Sign and submit the transaction
from xrpl.transaction import submit_and_wait

tx_response = submit_and_wait(my_payment_tx, client, test_wallet)
print(f'Payment of {xrp_to_send} XRP: {tx_response.status}')

# Step 6: Query the XRP ledger
# Retrieving the wallet balance after sending some XRP to another account
account_info_response = client.request(account_info)
account_balance_raw = account_info_response.result["account_data"]["Balance"]
account_balance = int(account_balance_raw) / 1000000

print(f'Account balance: {account_balance} XRP')