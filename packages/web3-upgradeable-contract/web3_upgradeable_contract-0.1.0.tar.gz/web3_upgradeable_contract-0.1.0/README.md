# Web3 upgradeable contract

[![codecov](https://codecov.io/github/tinom9/web3-upgradeable-contract/branch/master/graph/badge.svg?token=VID8VMTO4A)](https://codecov.io/github/tinom9/web3-upgradeable-contract)

Deploy contract with transparent upgradeable proxy schema. Inspired in `deployProxy`
implementation from [OpenZeppelin][1].

Python library to deploy Ethereum contracts using the transparent upgradeable proxy
schema with:
- Python `^3.10`
- Web3 `^6.0.0`

## Usage

```python
from web3 import Web3, middleware
from upgradeable_contract import UpgradeableContract
import solcx

box_contract = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Box {
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function store(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function retrieve() public view returns (uint256) {
        return value;
    }
}
"""

solcx.install_solc("0.8.19")
artifact = solcx.compile_source(
    box_contract,
    output_values=["abi", "bin"],
    solc_version="0.8.19",
)["<stdin>:Box"]
abi, bytecode = artifact["abi"], artifact["bin"]

private_key = "0x0000000000000000000000000000000000000000000000000000000000000000"
rpc_url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(rpc_url))
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address
w3.middleware_onion.add(middleware.construct_sign_and_send_raw_middleware(account))

contract: UpgradeableContract = w3.eth.contract(
    abi=abi, bytecode=bytecode, ContractFactoryClass=UpgradeableContract
)
implementation_address, admin_address, proxy_address = contract.deploy_proxy()

print(f"Implementation contract deployed at: {implementation_address}")
print(f"ProxyAdmin contract deployed at: {admin_address}")
print(f"TransparentUpgradeableProxy contract deployed at: {proxy_address}")
```

[1]: https://github.com/OpenZeppelin/openzeppelin-upgrades
