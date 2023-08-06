import json
import os

from upgradeable_contract.types import ContractArtifact


def _get_contract_artifact(contract: str) -> ContractArtifact:
    abs_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(abs_path, f"contracts/{contract}.json")
    with open(path) as f:
        return json.load(f)
