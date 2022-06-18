"""
This scripts sweeps assets from sub accounts to master accounts.
"""
from quidax import quidax


def sweeper():
    # Get master account sub id
    master_account = quidax.users.get_account_details("me")['data']['id']

    # Get list of available assets on quidax0
    all_assets = ['usdc', 'busd', 'usdt']

    # Get sub users
    sub_users_id = list(
        set([assets['id'] for assets in quidax.users.all_sub_account()['data']]))

    # Loop through users
    for user in sub_users_id:

        # Loop through assets and get balance
        for asset in all_assets:

            user_wallet_info = quidax.wallets.fetch_a_specific_currency_wallet(
                user, asset)

            currency = user_wallet_info['data']['currency']

            balance = float(user_wallet_info['data']['balance'])

            data = {
                "currency": currency,
                "amount": user_wallet_info['data']['balance'],
                "transaction_note": "sweeping bot",
                "fund_uid": master_account,
                "narration": "sweep",
            }

            if balance > 0:
                # If balance available, send it to master account.
                quidax.withdrawal.create_a_withdrawal(
                    user, **data,
                )

                print(f"user balance: {currency}:{user}:{balance}")
            else:
                print("no asset present.")


        print("\n")

if __name__ == "__main__":
    sweeper()
