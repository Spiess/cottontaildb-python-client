from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IndexType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BTREE: _ClassVar[IndexType]
    BTREE_UQ: _ClassVar[IndexType]
    LUCENE: _ClassVar[IndexType]
    VAF: _ClassVar[IndexType]
    PQ: _ClassVar[IndexType]
    IVFPQ: _ClassVar[IndexType]
    LSH: _ClassVar[IndexType]

class TransactionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    READ_WRITE: _ClassVar[TransactionMode]
    READONLY: _ClassVar[TransactionMode]

class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOOLEAN: _ClassVar[Type]
    BYTE: _ClassVar[Type]
    SHORT: _ClassVar[Type]
    INTEGER: _ClassVar[Type]
    LONG: _ClassVar[Type]
    FLOAT: _ClassVar[Type]
    DOUBLE: _ClassVar[Type]
    DATE: _ClassVar[Type]
    STRING: _ClassVar[Type]
    UUID: _ClassVar[Type]
    COMPLEX32: _ClassVar[Type]
    COMPLEX64: _ClassVar[Type]
    DOUBLE_VECTOR: _ClassVar[Type]
    FLOAT_VECTOR: _ClassVar[Type]
    LONG_VECTOR: _ClassVar[Type]
    INTEGER_VECTOR: _ClassVar[Type]
    BOOLEAN_VECTOR: _ClassVar[Type]
    COMPLEX32_VECTOR: _ClassVar[Type]
    COMPLEX64_VECTOR: _ClassVar[Type]
    SHORT_VECTOR: _ClassVar[Type]
    HALF_VECTOR: _ClassVar[Type]
    BYTESTRING: _ClassVar[Type]
BTREE: IndexType
BTREE_UQ: IndexType
LUCENE: IndexType
VAF: IndexType
PQ: IndexType
IVFPQ: IndexType
LSH: IndexType
READ_WRITE: TransactionMode
READONLY: TransactionMode
BOOLEAN: Type
BYTE: Type
SHORT: Type
INTEGER: Type
LONG: Type
FLOAT: Type
DOUBLE: Type
DATE: Type
STRING: Type
UUID: Type
COMPLEX32: Type
COMPLEX64: Type
DOUBLE_VECTOR: Type
FLOAT_VECTOR: Type
LONG_VECTOR: Type
INTEGER_VECTOR: Type
BOOLEAN_VECTOR: Type
COMPLEX32_VECTOR: Type
COMPLEX64_VECTOR: Type
SHORT_VECTOR: Type
HALF_VECTOR: Type
BYTESTRING: Type

class SchemaName(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class FunctionName(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class EntityName(_message.Message):
    __slots__ = ("schema", "name")
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    schema: SchemaName
    name: str
    def __init__(self, schema: _Optional[_Union[SchemaName, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class IndexName(_message.Message):
    __slots__ = ("entity", "name")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    entity: EntityName
    name: str
    def __init__(self, entity: _Optional[_Union[EntityName, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class ColumnName(_message.Message):
    __slots__ = ("entity", "name")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    entity: EntityName
    name: str
    def __init__(self, entity: _Optional[_Union[EntityName, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class BeginTransaction(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: TransactionMode
    def __init__(self, mode: _Optional[_Union[TransactionMode, str]] = ...) -> None: ...

class RequestMetadata(_message.Message):
    __slots__ = ("transactionId", "queryId", "parallelHint", "indexHint", "policyHint", "noOptimiseHint")
    class ParallelismHint(_message.Message):
        __slots__ = ("limit",)
        LIMIT_FIELD_NUMBER: _ClassVar[int]
        limit: int
        def __init__(self, limit: _Optional[int] = ...) -> None: ...
    class IndexHint(_message.Message):
        __slots__ = ("name", "type", "disallow")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        DISALLOW_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: IndexType
        disallow: bool
        def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[IndexType, str]] = ..., disallow: bool = ...) -> None: ...
    class PolicyHint(_message.Message):
        __slots__ = ("weightIo", "weightCpu", "weightMemory", "weightAccuracy")
        WEIGHTIO_FIELD_NUMBER: _ClassVar[int]
        WEIGHTCPU_FIELD_NUMBER: _ClassVar[int]
        WEIGHTMEMORY_FIELD_NUMBER: _ClassVar[int]
        WEIGHTACCURACY_FIELD_NUMBER: _ClassVar[int]
        weightIo: float
        weightCpu: float
        weightMemory: float
        weightAccuracy: float
        def __init__(self, weightIo: _Optional[float] = ..., weightCpu: _Optional[float] = ..., weightMemory: _Optional[float] = ..., weightAccuracy: _Optional[float] = ...) -> None: ...
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    QUERYID_FIELD_NUMBER: _ClassVar[int]
    PARALLELHINT_FIELD_NUMBER: _ClassVar[int]
    INDEXHINT_FIELD_NUMBER: _ClassVar[int]
    POLICYHINT_FIELD_NUMBER: _ClassVar[int]
    NOOPTIMISEHINT_FIELD_NUMBER: _ClassVar[int]
    transactionId: int
    queryId: str
    parallelHint: RequestMetadata.ParallelismHint
    indexHint: RequestMetadata.IndexHint
    policyHint: RequestMetadata.PolicyHint
    noOptimiseHint: bool
    def __init__(self, transactionId: _Optional[int] = ..., queryId: _Optional[str] = ..., parallelHint: _Optional[_Union[RequestMetadata.ParallelismHint, _Mapping]] = ..., indexHint: _Optional[_Union[RequestMetadata.IndexHint, _Mapping]] = ..., policyHint: _Optional[_Union[RequestMetadata.PolicyHint, _Mapping]] = ..., noOptimiseHint: bool = ...) -> None: ...

class ResponseMetadata(_message.Message):
    __slots__ = ("transactionId", "transactionMode", "queryId", "planDuration", "planScore", "queryDuration")
    TRANSACTIONID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONMODE_FIELD_NUMBER: _ClassVar[int]
    QUERYID_FIELD_NUMBER: _ClassVar[int]
    PLANDURATION_FIELD_NUMBER: _ClassVar[int]
    PLANSCORE_FIELD_NUMBER: _ClassVar[int]
    QUERYDURATION_FIELD_NUMBER: _ClassVar[int]
    transactionId: int
    transactionMode: TransactionMode
    queryId: str
    planDuration: int
    planScore: float
    queryDuration: int
    def __init__(self, transactionId: _Optional[int] = ..., transactionMode: _Optional[_Union[TransactionMode, str]] = ..., queryId: _Optional[str] = ..., planDuration: _Optional[int] = ..., planScore: _Optional[float] = ..., queryDuration: _Optional[int] = ...) -> None: ...

class Literal(_message.Message):
    __slots__ = ("nullData", "booleanData", "intData", "longData", "floatData", "doubleData", "stringData", "dateData", "uuidData", "complex32Data", "complex64Data", "vectorData", "byteStringData")
    NULLDATA_FIELD_NUMBER: _ClassVar[int]
    BOOLEANDATA_FIELD_NUMBER: _ClassVar[int]
    INTDATA_FIELD_NUMBER: _ClassVar[int]
    LONGDATA_FIELD_NUMBER: _ClassVar[int]
    FLOATDATA_FIELD_NUMBER: _ClassVar[int]
    DOUBLEDATA_FIELD_NUMBER: _ClassVar[int]
    STRINGDATA_FIELD_NUMBER: _ClassVar[int]
    DATEDATA_FIELD_NUMBER: _ClassVar[int]
    UUIDDATA_FIELD_NUMBER: _ClassVar[int]
    COMPLEX32DATA_FIELD_NUMBER: _ClassVar[int]
    COMPLEX64DATA_FIELD_NUMBER: _ClassVar[int]
    VECTORDATA_FIELD_NUMBER: _ClassVar[int]
    BYTESTRINGDATA_FIELD_NUMBER: _ClassVar[int]
    nullData: Null
    booleanData: bool
    intData: int
    longData: int
    floatData: float
    doubleData: float
    stringData: str
    dateData: int
    uuidData: Uuid
    complex32Data: Complex32
    complex64Data: Complex64
    vectorData: Vector
    byteStringData: bytes
    def __init__(self, nullData: _Optional[_Union[Null, _Mapping]] = ..., booleanData: bool = ..., intData: _Optional[int] = ..., longData: _Optional[int] = ..., floatData: _Optional[float] = ..., doubleData: _Optional[float] = ..., stringData: _Optional[str] = ..., dateData: _Optional[int] = ..., uuidData: _Optional[_Union[Uuid, _Mapping]] = ..., complex32Data: _Optional[_Union[Complex32, _Mapping]] = ..., complex64Data: _Optional[_Union[Complex64, _Mapping]] = ..., vectorData: _Optional[_Union[Vector, _Mapping]] = ..., byteStringData: _Optional[bytes] = ...) -> None: ...

class LiteralList(_message.Message):
    __slots__ = ("literal",)
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    literal: _containers.RepeatedCompositeFieldContainer[Literal]
    def __init__(self, literal: _Optional[_Iterable[_Union[Literal, _Mapping]]] = ...) -> None: ...

class Expression(_message.Message):
    __slots__ = ("literal", "literalList", "column", "function", "query")
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    LITERALLIST_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    literal: Literal
    literalList: LiteralList
    column: ColumnName
    function: Function
    query: Query
    def __init__(self, literal: _Optional[_Union[Literal, _Mapping]] = ..., literalList: _Optional[_Union[LiteralList, _Mapping]] = ..., column: _Optional[_Union[ColumnName, _Mapping]] = ..., function: _Optional[_Union[Function, _Mapping]] = ..., query: _Optional[_Union[Query, _Mapping]] = ...) -> None: ...

class Function(_message.Message):
    __slots__ = ("name", "arguments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    name: FunctionName
    arguments: _containers.RepeatedCompositeFieldContainer[Expression]
    def __init__(self, name: _Optional[_Union[FunctionName, _Mapping]] = ..., arguments: _Optional[_Iterable[_Union[Expression, _Mapping]]] = ...) -> None: ...

class Expressions(_message.Message):
    __slots__ = ("expression",)
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    expression: _containers.RepeatedCompositeFieldContainer[Expression]
    def __init__(self, expression: _Optional[_Iterable[_Union[Expression, _Mapping]]] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ("half", "float", "double", "short", "int", "long", "bool", "complex32", "complex64")
    HALF_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    SHORT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    COMPLEX32_FIELD_NUMBER: _ClassVar[int]
    COMPLEX64_FIELD_NUMBER: _ClassVar[int]
    half: FloatVector
    float: FloatVector
    double: DoubleVector
    short: IntVector
    int: IntVector
    long: LongVector
    bool: BoolVector
    complex32: Complex32Vector
    complex64: Complex64Vector
    def __init__(self, half: _Optional[_Union[FloatVector, _Mapping]] = ..., float: _Optional[_Union[FloatVector, _Mapping]] = ..., double: _Optional[_Union[DoubleVector, _Mapping]] = ..., short: _Optional[_Union[IntVector, _Mapping]] = ..., int: _Optional[_Union[IntVector, _Mapping]] = ..., long: _Optional[_Union[LongVector, _Mapping]] = ..., bool: _Optional[_Union[BoolVector, _Mapping]] = ..., complex32: _Optional[_Union[Complex32Vector, _Mapping]] = ..., complex64: _Optional[_Union[Complex64Vector, _Mapping]] = ...) -> None: ...

class Null(_message.Message):
    __slots__ = ("type", "size")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    type: Type
    size: int
    def __init__(self, type: _Optional[_Union[Type, str]] = ..., size: _Optional[int] = ...) -> None: ...

class Uuid(_message.Message):
    __slots__ = ("leastSignificant", "mostSignificant")
    LEASTSIGNIFICANT_FIELD_NUMBER: _ClassVar[int]
    MOSTSIGNIFICANT_FIELD_NUMBER: _ClassVar[int]
    leastSignificant: int
    mostSignificant: int
    def __init__(self, leastSignificant: _Optional[int] = ..., mostSignificant: _Optional[int] = ...) -> None: ...

class Complex32(_message.Message):
    __slots__ = ("real", "imaginary")
    REAL_FIELD_NUMBER: _ClassVar[int]
    IMAGINARY_FIELD_NUMBER: _ClassVar[int]
    real: float
    imaginary: float
    def __init__(self, real: _Optional[float] = ..., imaginary: _Optional[float] = ...) -> None: ...

class Complex64(_message.Message):
    __slots__ = ("real", "imaginary")
    REAL_FIELD_NUMBER: _ClassVar[int]
    IMAGINARY_FIELD_NUMBER: _ClassVar[int]
    real: float
    imaginary: float
    def __init__(self, real: _Optional[float] = ..., imaginary: _Optional[float] = ...) -> None: ...

class FloatVector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, vector: _Optional[_Iterable[float]] = ...) -> None: ...

class DoubleVector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, vector: _Optional[_Iterable[float]] = ...) -> None: ...

class IntVector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, vector: _Optional[_Iterable[int]] = ...) -> None: ...

class LongVector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, vector: _Optional[_Iterable[int]] = ...) -> None: ...

class BoolVector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, vector: _Optional[_Iterable[bool]] = ...) -> None: ...

class Complex32Vector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedCompositeFieldContainer[Complex32]
    def __init__(self, vector: _Optional[_Iterable[_Union[Complex32, _Mapping]]] = ...) -> None: ...

class Complex64Vector(_message.Message):
    __slots__ = ("vector",)
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    vector: _containers.RepeatedCompositeFieldContainer[Complex64]
    def __init__(self, vector: _Optional[_Iterable[_Union[Complex64, _Mapping]]] = ...) -> None: ...

class CreateSchemaMessage(_message.Message):
    __slots__ = ("metadata", "schema", "mayExist")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    MAYEXIST_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    schema: SchemaName
    mayExist: bool
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., schema: _Optional[_Union[SchemaName, _Mapping]] = ..., mayExist: bool = ...) -> None: ...

class DropSchemaMessage(_message.Message):
    __slots__ = ("metadata", "schema")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    schema: SchemaName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., schema: _Optional[_Union[SchemaName, _Mapping]] = ...) -> None: ...

class ListSchemaMessage(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ...) -> None: ...

class CreateEntityMessage(_message.Message):
    __slots__ = ("metadata", "entity", "columns", "mayExist")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    MAYEXIST_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    columns: _containers.RepeatedCompositeFieldContainer[ColumnDefinition]
    mayExist: bool
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[ColumnDefinition, _Mapping]]] = ..., mayExist: bool = ...) -> None: ...

class DropEntityMessage(_message.Message):
    __slots__ = ("metadata", "entity")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ...) -> None: ...

class TruncateEntityMessage(_message.Message):
    __slots__ = ("metadata", "entity")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ...) -> None: ...

class AnalyzeEntityMessage(_message.Message):
    __slots__ = ("metadata", "entity")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    ASYNC_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ..., **kwargs) -> None: ...

class EntityDetailsMessage(_message.Message):
    __slots__ = ("metadata", "entity")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ...) -> None: ...

class IndexDetailsMessage(_message.Message):
    __slots__ = ("metadata", "index")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    index: IndexName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., index: _Optional[_Union[IndexName, _Mapping]] = ...) -> None: ...

class ListEntityMessage(_message.Message):
    __slots__ = ("metadata", "schema")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    schema: SchemaName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., schema: _Optional[_Union[SchemaName, _Mapping]] = ...) -> None: ...

class CreateIndexMessage(_message.Message):
    __slots__ = ("metadata", "entity", "type", "indexName", "columns", "params")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEXNAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    entity: EntityName
    type: IndexType
    indexName: str
    columns: _containers.RepeatedScalarFieldContainer[str]
    params: _containers.ScalarMap[str, str]
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., entity: _Optional[_Union[EntityName, _Mapping]] = ..., type: _Optional[_Union[IndexType, str]] = ..., indexName: _Optional[str] = ..., columns: _Optional[_Iterable[str]] = ..., params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DropIndexMessage(_message.Message):
    __slots__ = ("metadata", "index")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    index: IndexName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., index: _Optional[_Union[IndexName, _Mapping]] = ...) -> None: ...

class RebuildIndexMessage(_message.Message):
    __slots__ = ("metadata", "index")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ASYNC_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    index: IndexName
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., index: _Optional[_Union[IndexName, _Mapping]] = ..., **kwargs) -> None: ...

class ColumnDefinition(_message.Message):
    __slots__ = ("name", "type", "length", "primary", "nullable", "autoIncrement", "compression")
    class Compression(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[ColumnDefinition.Compression]
        NONE: _ClassVar[ColumnDefinition.Compression]
        LZ4: _ClassVar[ColumnDefinition.Compression]
        SNAPPY: _ClassVar[ColumnDefinition.Compression]
    DEFAULT: ColumnDefinition.Compression
    NONE: ColumnDefinition.Compression
    LZ4: ColumnDefinition.Compression
    SNAPPY: ColumnDefinition.Compression
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    AUTOINCREMENT_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    name: ColumnName
    type: Type
    length: int
    primary: bool
    nullable: bool
    autoIncrement: bool
    compression: ColumnDefinition.Compression
    def __init__(self, name: _Optional[_Union[ColumnName, _Mapping]] = ..., type: _Optional[_Union[Type, str]] = ..., length: _Optional[int] = ..., primary: bool = ..., nullable: bool = ..., autoIncrement: bool = ..., compression: _Optional[_Union[ColumnDefinition.Compression, str]] = ...) -> None: ...

class EntityDefinition(_message.Message):
    __slots__ = ("entity", "columns")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    entity: EntityName
    columns: _containers.RepeatedCompositeFieldContainer[ColumnDefinition]
    def __init__(self, entity: _Optional[_Union[EntityName, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[ColumnDefinition, _Mapping]]] = ...) -> None: ...

class InsertMessage(_message.Message):
    __slots__ = ("metadata", "elements")
    class InsertElement(_message.Message):
        __slots__ = ("column", "value")
        COLUMN_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        column: ColumnName
        value: Literal
        def __init__(self, column: _Optional[_Union[ColumnName, _Mapping]] = ..., value: _Optional[_Union[Literal, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    elements: _containers.RepeatedCompositeFieldContainer[InsertMessage.InsertElement]
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., elements: _Optional[_Iterable[_Union[InsertMessage.InsertElement, _Mapping]]] = ..., **kwargs) -> None: ...

class BatchInsertMessage(_message.Message):
    __slots__ = ("metadata", "columns", "inserts")
    class Insert(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[Literal]
        def __init__(self, values: _Optional[_Iterable[_Union[Literal, _Mapping]]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    INSERTS_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    columns: _containers.RepeatedCompositeFieldContainer[ColumnName]
    inserts: _containers.RepeatedCompositeFieldContainer[BatchInsertMessage.Insert]
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[ColumnName, _Mapping]]] = ..., inserts: _Optional[_Iterable[_Union[BatchInsertMessage.Insert, _Mapping]]] = ..., **kwargs) -> None: ...

class UpdateMessage(_message.Message):
    __slots__ = ("metadata", "where", "updates")
    class UpdateElement(_message.Message):
        __slots__ = ("column", "value")
        COLUMN_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        column: ColumnName
        value: Expression
        def __init__(self, column: _Optional[_Union[ColumnName, _Mapping]] = ..., value: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    WHERE_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    where: Where
    updates: _containers.RepeatedCompositeFieldContainer[UpdateMessage.UpdateElement]
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., where: _Optional[_Union[Where, _Mapping]] = ..., updates: _Optional[_Iterable[_Union[UpdateMessage.UpdateElement, _Mapping]]] = ..., **kwargs) -> None: ...

class DeleteMessage(_message.Message):
    __slots__ = ("metadata", "where")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    WHERE_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    where: Where
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., where: _Optional[_Union[Where, _Mapping]] = ..., **kwargs) -> None: ...

class QueryMessage(_message.Message):
    __slots__ = ("metadata", "query")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    metadata: RequestMetadata
    query: Query
    def __init__(self, metadata: _Optional[_Union[RequestMetadata, _Mapping]] = ..., query: _Optional[_Union[Query, _Mapping]] = ...) -> None: ...

class Query(_message.Message):
    __slots__ = ("projection", "where", "order", "limit", "skip")
    FROM_FIELD_NUMBER: _ClassVar[int]
    PROJECTION_FIELD_NUMBER: _ClassVar[int]
    WHERE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SKIP_FIELD_NUMBER: _ClassVar[int]
    projection: Projection
    where: Where
    order: Order
    limit: int
    skip: int
    def __init__(self, projection: _Optional[_Union[Projection, _Mapping]] = ..., where: _Optional[_Union[Where, _Mapping]] = ..., order: _Optional[_Union[Order, _Mapping]] = ..., limit: _Optional[int] = ..., skip: _Optional[int] = ..., **kwargs) -> None: ...

class QueryResponseMessage(_message.Message):
    __slots__ = ("metadata", "columns", "tuples")
    class Tuple(_message.Message):
        __slots__ = ("data",)
        DATA_FIELD_NUMBER: _ClassVar[int]
        data: _containers.RepeatedCompositeFieldContainer[Literal]
        def __init__(self, data: _Optional[_Iterable[_Union[Literal, _Mapping]]] = ...) -> None: ...
    METADATA_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    TUPLES_FIELD_NUMBER: _ClassVar[int]
    metadata: ResponseMetadata
    columns: _containers.RepeatedCompositeFieldContainer[ColumnDefinition]
    tuples: _containers.RepeatedCompositeFieldContainer[QueryResponseMessage.Tuple]
    def __init__(self, metadata: _Optional[_Union[ResponseMetadata, _Mapping]] = ..., columns: _Optional[_Iterable[_Union[ColumnDefinition, _Mapping]]] = ..., tuples: _Optional[_Iterable[_Union[QueryResponseMessage.Tuple, _Mapping]]] = ...) -> None: ...

class From(_message.Message):
    __slots__ = ("scan", "sample", "query")
    SCAN_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    scan: Scan
    sample: Sample
    query: Query
    def __init__(self, scan: _Optional[_Union[Scan, _Mapping]] = ..., sample: _Optional[_Union[Sample, _Mapping]] = ..., query: _Optional[_Union[Query, _Mapping]] = ...) -> None: ...

class Scan(_message.Message):
    __slots__ = ("entity", "start", "end")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    entity: EntityName
    start: int
    end: int
    def __init__(self, entity: _Optional[_Union[EntityName, _Mapping]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class Sample(_message.Message):
    __slots__ = ("entity", "seed", "probability")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    entity: EntityName
    seed: int
    probability: float
    def __init__(self, entity: _Optional[_Union[EntityName, _Mapping]] = ..., seed: _Optional[int] = ..., probability: _Optional[float] = ...) -> None: ...

class Projection(_message.Message):
    __slots__ = ("op", "elements")
    class ProjectionOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SELECT: _ClassVar[Projection.ProjectionOperation]
        SELECT_DISTINCT: _ClassVar[Projection.ProjectionOperation]
        COUNT: _ClassVar[Projection.ProjectionOperation]
        COUNT_DISTINCT: _ClassVar[Projection.ProjectionOperation]
        EXISTS: _ClassVar[Projection.ProjectionOperation]
        SUM: _ClassVar[Projection.ProjectionOperation]
        MAX: _ClassVar[Projection.ProjectionOperation]
        MIN: _ClassVar[Projection.ProjectionOperation]
        MEAN: _ClassVar[Projection.ProjectionOperation]
    SELECT: Projection.ProjectionOperation
    SELECT_DISTINCT: Projection.ProjectionOperation
    COUNT: Projection.ProjectionOperation
    COUNT_DISTINCT: Projection.ProjectionOperation
    EXISTS: Projection.ProjectionOperation
    SUM: Projection.ProjectionOperation
    MAX: Projection.ProjectionOperation
    MIN: Projection.ProjectionOperation
    MEAN: Projection.ProjectionOperation
    class ProjectionElement(_message.Message):
        __slots__ = ("alias", "expression")
        ALIAS_FIELD_NUMBER: _ClassVar[int]
        EXPRESSION_FIELD_NUMBER: _ClassVar[int]
        alias: ColumnName
        expression: Expression
        def __init__(self, alias: _Optional[_Union[ColumnName, _Mapping]] = ..., expression: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...
    OP_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    op: Projection.ProjectionOperation
    elements: _containers.RepeatedCompositeFieldContainer[Projection.ProjectionElement]
    def __init__(self, op: _Optional[_Union[Projection.ProjectionOperation, str]] = ..., elements: _Optional[_Iterable[_Union[Projection.ProjectionElement, _Mapping]]] = ...) -> None: ...

class Where(_message.Message):
    __slots__ = ("predicate",)
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    predicate: Predicate
    def __init__(self, predicate: _Optional[_Union[Predicate, _Mapping]] = ...) -> None: ...

class Predicate(_message.Message):
    __slots__ = ("literal", "comparison", "isnull")
    class Literal(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: bool
        def __init__(self, value: bool = ...) -> None: ...
    class IsNull(_message.Message):
        __slots__ = ("exp",)
        EXP_FIELD_NUMBER: _ClassVar[int]
        exp: Expression
        def __init__(self, exp: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...
    class Comparison(_message.Message):
        __slots__ = ("lexp", "operator", "rexp")
        class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            EQUAL: _ClassVar[Predicate.Comparison.Operator]
            NOTEQUAL: _ClassVar[Predicate.Comparison.Operator]
            GREATER: _ClassVar[Predicate.Comparison.Operator]
            LESS: _ClassVar[Predicate.Comparison.Operator]
            GEQUAL: _ClassVar[Predicate.Comparison.Operator]
            LEQUAL: _ClassVar[Predicate.Comparison.Operator]
            IN: _ClassVar[Predicate.Comparison.Operator]
            BETWEEN: _ClassVar[Predicate.Comparison.Operator]
            LIKE: _ClassVar[Predicate.Comparison.Operator]
            MATCH: _ClassVar[Predicate.Comparison.Operator]
        EQUAL: Predicate.Comparison.Operator
        NOTEQUAL: Predicate.Comparison.Operator
        GREATER: Predicate.Comparison.Operator
        LESS: Predicate.Comparison.Operator
        GEQUAL: Predicate.Comparison.Operator
        LEQUAL: Predicate.Comparison.Operator
        IN: Predicate.Comparison.Operator
        BETWEEN: Predicate.Comparison.Operator
        LIKE: Predicate.Comparison.Operator
        MATCH: Predicate.Comparison.Operator
        LEXP_FIELD_NUMBER: _ClassVar[int]
        OPERATOR_FIELD_NUMBER: _ClassVar[int]
        REXP_FIELD_NUMBER: _ClassVar[int]
        lexp: Expression
        operator: Predicate.Comparison.Operator
        rexp: Expression
        def __init__(self, lexp: _Optional[_Union[Expression, _Mapping]] = ..., operator: _Optional[_Union[Predicate.Comparison.Operator, str]] = ..., rexp: _Optional[_Union[Expression, _Mapping]] = ...) -> None: ...
    class And(_message.Message):
        __slots__ = ("p1", "p2")
        P1_FIELD_NUMBER: _ClassVar[int]
        P2_FIELD_NUMBER: _ClassVar[int]
        p1: Predicate
        p2: Predicate
        def __init__(self, p1: _Optional[_Union[Predicate, _Mapping]] = ..., p2: _Optional[_Union[Predicate, _Mapping]] = ...) -> None: ...
    class Or(_message.Message):
        __slots__ = ("p1", "p2")
        P1_FIELD_NUMBER: _ClassVar[int]
        P2_FIELD_NUMBER: _ClassVar[int]
        p1: Predicate
        p2: Predicate
        def __init__(self, p1: _Optional[_Union[Predicate, _Mapping]] = ..., p2: _Optional[_Union[Predicate, _Mapping]] = ...) -> None: ...
    class Not(_message.Message):
        __slots__ = ("p",)
        P_FIELD_NUMBER: _ClassVar[int]
        p: Predicate
        def __init__(self, p: _Optional[_Union[Predicate, _Mapping]] = ...) -> None: ...
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    COMPARISON_FIELD_NUMBER: _ClassVar[int]
    ISNULL_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    NOT_FIELD_NUMBER: _ClassVar[int]
    literal: Predicate.Literal
    comparison: Predicate.Comparison
    isnull: Predicate.IsNull
    def __init__(self, literal: _Optional[_Union[Predicate.Literal, _Mapping]] = ..., comparison: _Optional[_Union[Predicate.Comparison, _Mapping]] = ..., isnull: _Optional[_Union[Predicate.IsNull, _Mapping]] = ..., **kwargs) -> None: ...

class Order(_message.Message):
    __slots__ = ("components",)
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ASCENDING: _ClassVar[Order.Direction]
        DESCENDING: _ClassVar[Order.Direction]
    ASCENDING: Order.Direction
    DESCENDING: Order.Direction
    class Component(_message.Message):
        __slots__ = ("column", "direction")
        COLUMN_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        column: ColumnName
        direction: Order.Direction
        def __init__(self, column: _Optional[_Union[ColumnName, _Mapping]] = ..., direction: _Optional[_Union[Order.Direction, str]] = ...) -> None: ...
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    components: _containers.RepeatedCompositeFieldContainer[Order.Component]
    def __init__(self, components: _Optional[_Iterable[_Union[Order.Component, _Mapping]]] = ...) -> None: ...
