"""
This scripts sweeps assets from sub accounts to master accounts.
"""
from quidax import quidax


def sweeper():
    # Get master account sub id
    master_account = quidax.users.get_account_details("me")['data']['id']

    # Get list of available assets on quidax
    all_assets = ['usdc', 'busd', 'usdt']

    # Fetch all sub accounts
    all_accounts_obj = quidax.users.all_sub_account()

    # Get user objects
    all_accounts_data = all_accounts_obj.get("data", [])

    # Get sub users
    sub_users_id = list(set([assets['id'] for assets in all_accounts_data]))

    # Loop through users
    for user in sub_users_id:

        # Loop through assets and get balance
        for asset in all_assets:

            # Fetch user wallet objects
            user_wallet_info = quidax.wallets.fetch_a_specific_currency_wallet(
                user, asset,
            )
            
            # Fetch currency
            currency = user_wallet_info['data']['currency']

            # Fetch user balance
            balance = float(user_wallet_info['data']['balance'])

            # Data payload.
            data = {
                "currency": currency,
                "amount": user_wallet_info['data']['balance'],
                "transaction_note": "sweeping bot",
                "fund_uid": master_account,
                "narration": "sweep",
            }

            # if balance is greater than zero
            if balance > 0:

                # If balance available, send it to master account.
                quidax.withdrawal.create_a_withdrawal(
                    user, **data,
                )

                # Print user balance
                print(f"user balance: {currency} : {user} : {balance}")
            else:

                # Print no asset present
                print("no asset present.")


        print("\n")

if __name__ == "__main__":
    sweeper()
