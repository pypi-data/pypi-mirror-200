from pydantic.fields import Field
from pydantic.main import BaseModel

from models.common import HexToInt


class Block(BaseModel):
    """Ethereum Block Model."""

    difficulty: HexToInt
    extra_data: str = Field(alias="extraData")
    gas_limit: HexToInt = Field(alias="gasLimit")
    gas_used: HexToInt = Field(alias="gasUsed")
    hash: str
    logs_bloom: str = Field(alias="logsBloom")
    miner: str
    mix_hash: str = Field(alias="mixHash")
    nonce: str
    number: HexToInt
    parent_hash: str = Field(alias="parentHash")
    receipts_root: str = Field(alias="receiptsRoot")
    sha3_uncles: str = Field(alias="sha3Uncles")
    size: HexToInt
    state_root: str = Field(alias="stateRoot")
    timestamp: HexToInt
    total_difficulty: HexToInt = Field(alias="totalDifficulty")
    transactions_root: str = Field(alias="transactionsRoot")
