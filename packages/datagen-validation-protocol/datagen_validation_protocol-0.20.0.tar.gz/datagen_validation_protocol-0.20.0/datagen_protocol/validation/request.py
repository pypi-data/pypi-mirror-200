from typing import List, Union

from datagen_protocol.schema import DataSequence
from datagen_protocol.schema import request as core_request_schema
from datagen_protocol.validation.humans.human import HumanDatapoint as ValidationHumanDatapoint


class DataRequest(core_request_schema.DataRequest):
    datapoints: List[Union[DataSequence, ValidationHumanDatapoint]]


core_request_schema.DataRequest = DataRequest
