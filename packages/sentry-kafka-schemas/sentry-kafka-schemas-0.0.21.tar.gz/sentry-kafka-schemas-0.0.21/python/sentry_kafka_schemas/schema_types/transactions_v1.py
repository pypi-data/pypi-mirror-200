from typing import TypedDict, Dict, List, Literal, Tuple, Any, Union
from typing_extensions import Required


class TransactionEvent(TypedDict, total=False):
    """transaction_event."""

    group_id: None
    group_ids: List[int]
    event_id: str
    organization_id: int
    project_id: int
    message: str
    platform: str
    datetime: str
    """format: date-time"""

    data: "_TransactionEventData"
    primary_hash: None
    retention_days: None
    occurrence_id: None
    occurrence_data: Dict[str, Any]
    is_new: bool
    is_regression: bool
    is_new_group_environment: bool
    queue: str
    skip_consume: bool
    group_states: None


class _TransactionEventData(TypedDict, total=False):
    event_id: Required[str]
    """Required property"""

    level: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""

    type: Required[str]
    """Required property"""

    transaction: Required[str]
    """Required property"""

    transaction_info: Required["_TransactionEventDataTransactionInfo"]
    """Required property"""

    logger: Required[str]
    """Required property"""

    platform: Required[str]
    """Required property"""

    timestamp: Required[Union[int, float]]
    """Required property"""

    start_timestamp: Required[Union[int, float]]
    """Required property"""

    received: Required[Union[int, float]]
    """Required property"""

    release: Required[str]
    """Required property"""

    environment: Required[str]
    """Required property"""

    contexts: Required["_TransactionEventDataContexts"]
    """Required property"""

    tags: Required[List[List[Union[None, str]]]]
    """Required property"""

    extra: Required["_TransactionEventDataExtra"]
    """Required property"""

    sdk: Required["_TransactionEventDataSdk"]
    """Required property"""

    key_id: Required[str]
    """Required property"""

    project: Required[int]
    """Required property"""

    grouping_config: Required["_TransactionEventDataGroupingConfig"]
    """Required property"""

    spans: Required[List["_TransactionEventDataSpansItem"]]
    """Required property"""

    measurements: Required["_TransactionEventDataMeasurements"]
    """Required property"""

    breakdowns: Required["_TransactionEventDataBreakdowns"]
    """Required property"""

    _metrics: Required["_TransactionEventDataMetrics"]
    """Required property"""

    span_grouping_config: Required["_TransactionEventDataSpanGroupingConfig"]
    """Required property"""

    culprit: Required[str]
    """Required property"""

    metadata: Required["_TransactionEventDataMetadata"]
    """Required property"""

    title: Required[str]
    """Required property"""

    location: Required[str]
    """Required property"""

    hashes: Required[List[str]]
    """Required property"""

    nodestore_insert: Required[Union[int, float]]
    """Required property"""



class _TransactionEventDataBreakdowns(TypedDict, total=False):
    span_ops: Required[Dict[str, "_TransactionEventDataMeasurementsNumOfSpans"]]
    """Required property"""



class _TransactionEventDataContexts(TypedDict, total=False):
    runtime: Required["_TransactionEventDataContextsRuntime"]
    """Required property"""

    trace: Required["_TransactionEventDataContextsTrace"]
    """Required property"""



class _TransactionEventDataContextsRuntime(TypedDict, total=False):
    name: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""

    build: Required[str]
    """Required property"""

    type: Required[str]
    """Required property"""



class _TransactionEventDataContextsTrace(TypedDict, total=False):
    trace_id: Required[str]
    """Required property"""

    span_id: Required[str]
    """Required property"""

    parent_span_id: Required[str]
    """Required property"""

    op: Required[str]
    """Required property"""

    status: Required[str]
    """Required property"""

    exclusive_time: Required[Union[int, float]]
    """Required property"""

    type: Required[str]
    """Required property"""

    hash: Required[str]
    """Required property"""



_TransactionEventDataExtra = Union[Dict[str, Any], None]
"""
 Arbitrary extra information set by the user.

 ```json
 {
     "extra": {
         "my_key": 1,
         "some_other_value": "foo bar"
     }
 }```
"""



class _TransactionEventDataGroupingConfig(TypedDict, total=False):
    enhancements: Required[str]
    """Required property"""

    id: Required[str]
    """Required property"""



class _TransactionEventDataMeasurements(TypedDict, total=False):
    num_of_spans: Required["_TransactionEventDataMeasurementsNumOfSpans"]
    """Required property"""



class _TransactionEventDataMeasurementsNumOfSpans(TypedDict, total=False):
    value: Required[Union[int, float]]
    """Required property"""

    unit: Required[str]
    """Required property"""



class _TransactionEventDataMetadata(TypedDict, total=False):
    title: Required[str]
    """Required property"""

    location: Required[str]
    """Required property"""



_TransactionEventDataMetrics = TypedDict('_TransactionEventDataMetrics', {
    # Required property
    'bytes.ingested.event': Required[int],
    # Required property
    'bytes.stored.event': Required[int],
}, total=False)


class _TransactionEventDataSdk(TypedDict, total=False):
    name: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""

    integrations: Required[List[str]]
    """Required property"""

    packages: Required[List["_TransactionEventDataSdkPackagesItem"]]
    """Required property"""



class _TransactionEventDataSdkPackagesItem(TypedDict, total=False):
    name: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""



class _TransactionEventDataSpanGroupingConfig(TypedDict, total=False):
    id: Required[str]
    """Required property"""



class _TransactionEventDataSpansItem(TypedDict, total=False):
    timestamp: Required[Union[int, float]]
    """Required property"""

    start_timestamp: Required[Union[int, float]]
    """Required property"""

    exclusive_time: Required[Union[int, float]]
    """Required property"""

    description: Required[str]
    """Required property"""

    op: Required[str]
    """Required property"""

    span_id: Required[str]
    """Required property"""

    parent_span_id: Required[str]
    """Required property"""

    trace_id: Required[str]
    """Required property"""

    same_process_as_parent: Required[bool]
    """Required property"""

    tags: Required[None]
    """Required property"""

    data: Required[None]
    """Required property"""

    hash: Required[str]
    """Required property"""



class _TransactionEventDataTransactionInfo(TypedDict, total=False):
    source: Required[str]
    """Required property"""

