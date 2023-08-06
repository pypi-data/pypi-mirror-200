from typing import Any, Type

from web3.contract.contract import Contract
from web3.types import ChecksumAddress, HexBytes, HexStr, TxParams

from upgradeable_contract.utils import _get_contract_artifact


class UpgradeableContract(Contract):
    implementation_contract: "Contract" | Type["Contract"] | None = None
    implementation_deploy_tx: HexBytes | None = None
    admin_contract: "Contract" | Type["Contract"] | None = None
    admin_deploy_tx: HexBytes | None = None
    proxy_contract: "Contract" | Type["Contract"] | None = None
    proxy_deploy_tx: HexBytes | None = None

    @classmethod
    def deploy_implementation(
        cls, transaction: TxParams | None = None, *args: Any, **kwargs: Any
    ) -> HexBytes:
        if cls.bytecode is None:
            raise ValueError(
                "Cannot call deploy_implementation on a contract that does not have "
                "'bytecode' associated with it"
            )
        if cls.abi is None:
            raise ValueError(
                "Cannot call deploy_implementation on a contract that does not have "
                "'ABI' associated with it"
            )
        cls.implementation_contract = cls.w3.eth.contract(
            abi=cls.abi, bytecode=cls.bytecode
        )
        cls.implementation_deploy_tx = cls.implementation_contract.constructor(
            *args, **kwargs
        ).transact(transaction)
        return cls.implementation_deploy_tx

    @classmethod
    def deploy_proxy_admin(cls, transaction: TxParams | None = None) -> HexBytes:
        PROXY_ADMIN = _get_contract_artifact("ProxyAdmin")
        cls.admin_contract = cls.w3.eth.contract(
            abi=PROXY_ADMIN["abi"],
            bytecode=PROXY_ADMIN["bytecode"],
        )
        deploy_tx = cls.admin_contract.constructor().transact(transaction)
        cls.admin_deploy_tx = deploy_tx
        return deploy_tx

    @classmethod
    def deploy_transparent_upgradeable_proxy(
        cls,
        implementation_address: ChecksumAddress,
        admin_address: ChecksumAddress,
        data: bytes | HexStr | str = "0x",
        transaction: TxParams | None = None,
    ) -> HexBytes:
        TRANSPARENT_UPGRADEABLE_PROXY = _get_contract_artifact(
            "TransparentUpgradeableProxy"
        )
        cls.proxy_contract = cls.w3.eth.contract(
            abi=TRANSPARENT_UPGRADEABLE_PROXY["abi"],
            bytecode=TRANSPARENT_UPGRADEABLE_PROXY["bytecode"],
        )
        deploy_tx = cls.proxy_contract.constructor(
            implementation_address, admin_address, data
        ).transact(transaction)
        cls.proxy_deploy_tx = deploy_tx
        return deploy_tx

    @classmethod
    def deploy_proxy(
        cls,
        data: bytes | HexStr | str = "0x",
        transaction: TxParams | None = None,
        *args: Any,
        **kwargs: Any
    ) -> tuple[ChecksumAddress, ChecksumAddress, ChecksumAddress]:
        if cls.bytecode is None:
            raise ValueError(
                "Cannot call deploy_proxy on a contract that does not have "
                "'bytecode' associated with it"
            )
        if cls.abi is None:
            raise ValueError(
                "Cannot call deploy_proxy on a contract that does not have "
                "'ABI' associated with it"
            )
        if not cls.implementation_contract:
            cls.deploy_implementation(transaction, *args, **kwargs)
        if not cls.implementation_contract.address:
            implementation_tx_receipt = cls.w3.eth.wait_for_transaction_receipt(
                cls.implementation_deploy_tx
            )
            cls.implementation_contract = cls.w3.eth.contract(
                address=implementation_tx_receipt.contractAddress,
                abi=cls.implementation_contract.abi,
            )
        if not cls.admin_contract:
            cls.deploy_proxy_admin(transaction, *args, **kwargs)
        if not cls.admin_contract.address:
            admin_tx_receipt = cls.w3.eth.wait_for_transaction_receipt(
                cls.admin_deploy_tx
            )
            cls.admin_contract = cls.w3.eth.contract(
                address=admin_tx_receipt.contractAddress,
                abi=cls.admin_contract.abi,
            )
        cls.deploy_transparent_upgradeable_proxy(
            cls.implementation_contract.address,
            cls.admin_contract.address,
            data,
            transaction,
        )
        proxy_tx_receipt = cls.w3.eth.wait_for_transaction_receipt(cls.proxy_deploy_tx)
        cls.proxy_contract = cls.w3.eth.contract(
            address=proxy_tx_receipt.contractAddress,
            abi=cls.proxy_contract.abi + cls.implementation_contract.abi,
        )
        return (
            cls.implementation_contract.address,
            cls.admin_contract.address,
            cls.proxy_contract.address,
        )
