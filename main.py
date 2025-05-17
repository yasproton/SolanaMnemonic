from mnemonic import Mnemonic
from solana.rpc.api import Client
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def generate_solana_recovery_phrases(n=10):
    mnemo = Mnemonic("english")
    phrases = []
    for _ in range(n):
        phrase = mnemo.generate(strength=128)
        phrases.append(phrase)
    return phrases

def get_solana_pubkey_from_phrase(phrase):
    try:
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
        acct = bip44_def_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        pubkey = acct.PublicKey().ToAddress()
        return pubkey
    except Exception as e:
        print(f"Errore nel derivare il pubkey dalla frase: {e}")
        return None

def get_solana_balance(pubkey, client):
    try:
        resp = client.get_balance(pubkey)
        if resp.get("result") and resp["result"].get("value") is not None:
            lamports = resp["result"]["value"]
            sol = lamports / 1_000_000_000
            return sol
    except Exception as e:
        print(f"Errore nel recuperare il saldo: {e}")
    return 0

if __name__ == "__main__":
    client = Client("https://api.mainnet-beta.solana.com")
    num_phrases = 100

    phrases = generate_solana_recovery_phrases(num_phrases)
    count_with_balance = 0

    for phrase in phrases:
        pubkey = get_solana_pubkey_from_phrase(phrase)
        if not pubkey:
            continue
        balance = get_solana_balance(pubkey, client)
        if balance > 0:
            count_with_balance += 1
            print(f"Recovery Phrase: {phrase}")
            print(f"Address: {pubkey}")
            print(f"Balance: {balance} SOL\n")

    print(f"Trovati {count_with_balance} wallet con saldo su {num_phrases} frasi generate.")
