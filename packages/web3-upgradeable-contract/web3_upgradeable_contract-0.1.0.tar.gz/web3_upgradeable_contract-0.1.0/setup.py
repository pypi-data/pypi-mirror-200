# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upgradeable_contract']

package_data = \
{'': ['*'], 'upgradeable_contract': ['contracts/*']}

install_requires = \
['web3>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'web3-upgradeable-contract',
    'version': '0.1.0',
    'description': 'Deploy contract with transparent upgradeable proxy schema',
    'long_description': '# Web3 upgradeable contract\n\n[![codecov](https://codecov.io/github/tinom9/web3-upgradeable-contract/branch/master/graph/badge.svg?token=VID8VMTO4A)](https://codecov.io/github/tinom9/web3-upgradeable-contract)\n\nDeploy contract with transparent upgradeable proxy schema. Inspired in `deployProxy`\nimplementation from [OpenZeppelin][1].\n\nPython library to deploy Ethereum contracts using the transparent upgradeable proxy\nschema with:\n- Python `^3.10`\n- Web3 `^6.0.0`\n\n## Usage\n\n```python\nfrom web3 import Web3, middleware\nfrom upgradeable_contract import UpgradeableContract\nimport solcx\n\nbox_contract = """\n// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\ncontract Box {\n    uint256 private value;\n\n    event ValueChanged(uint256 newValue);\n\n    function store(uint256 newValue) public {\n        value = newValue;\n        emit ValueChanged(newValue);\n    }\n\n    function retrieve() public view returns (uint256) {\n        return value;\n    }\n}\n"""\n\nsolcx.install_solc("0.8.19")\nartifact = solcx.compile_source(\n    box_contract,\n    output_values=["abi", "bin"],\n    solc_version="0.8.19",\n)["<stdin>:Box"]\nabi, bytecode = artifact["abi"], artifact["bin"]\n\nprivate_key = "0x0000000000000000000000000000000000000000000000000000000000000000"\nrpc_url = "http://127.0.0.1:8545"\nw3 = Web3(Web3.HTTPProvider(rpc_url))\naccount = w3.eth.account.from_key(private_key)\nw3.eth.default_account = account.address\nw3.middleware_onion.add(middleware.construct_sign_and_send_raw_middleware(account))\n\ncontract: UpgradeableContract = w3.eth.contract(\n    abi=abi, bytecode=bytecode, ContractFactoryClass=UpgradeableContract\n)\nimplementation_address, admin_address, proxy_address = contract.deploy_proxy()\n\nprint(f"Implementation contract deployed at: {implementation_address}")\nprint(f"ProxyAdmin contract deployed at: {admin_address}")\nprint(f"TransparentUpgradeableProxy contract deployed at: {proxy_address}")\n```\n\n[1]: https://github.com/OpenZeppelin/openzeppelin-upgrades\n',
    'author': 'Tino Martínez Molina',
    'author_email': 'tino@martinezmolina.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tinom9/web3-upgradeable-contract',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
