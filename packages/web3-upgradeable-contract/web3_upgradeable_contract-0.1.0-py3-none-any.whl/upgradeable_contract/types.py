from typing import TypedDict


class ContractArtifact(TypedDict):
    abi: list
    bytecode: str
