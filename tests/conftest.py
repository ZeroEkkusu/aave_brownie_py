import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, chain


@pytest.fixture(scope="module")
def test_only_locally():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    else:
        chain.reset()


@pytest.fixture(scope="module")
def dont_test_locally():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
