[
    {
        "fqn_list": "alembic_postgresql_enum/connection.py/get_connection",
        "new_code": """
import sqlalchemy.engine
from typing import Iterator

def get_connection(operations) -> Iterator[sqlalchemy.engine.Connection]:
    connection = sqlalchemy.create_engine('postgresql://username:password@localhost:5432/database').connect()
    yield connection
    connection.close()
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/compare_dispatch.py/compare_enums",
        "new_code": """
from alembic_postgresql_enum import AutogenContext, UpgradeOps
from typing import Iterable, Union

def compare_enums(autogen_context: AutogenContext, upgrade_ops: UpgradeOps, schema_names: Iterable[Union[str, None]]):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_create_type_false.py/ReprWorkaround/__repr__",
        "new_code": """
class ReprWorkaround:
    def __repr__(self):
        return "ReprWorkaround()"
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_create_type_false.py/get_replacement_type",
        "new_code": """
def get_replacement_type(column_type):
    return column_type
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_create_type_false.py/inject_repr_into_enums",
        "new_code": """
from sqlalchemy.sql.schema import Column

def inject_repr_into_enums(column: Column):
    column.type.__class__.__repr__ = ReprWorkaround.__repr__
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_create_type_false.py/add_create_type_false",
        "new_code": """
from alembic_postgresql_enum import UpgradeOps
from sqlalchemy.sql.schema import Column

def add_create_type_false(upgrade_ops: UpgradeOps):
    for op in upgrade_ops.ops:
        if isinstance(op, ops.CreateTableOp):
            for column in op.columns:
                inject_repr_into_enums(column)
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_postgres_using_to_text.py/PostgresUsingAlterColumnOp/reverse",
        "new_code": """
class PostgresUsingAlterColumnOp:
    def reverse(self):
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_postgres_using_to_text.py/_postgres_using_alter_column",
        "new_code": """
from alembic_postgresql_enum import AutogenContext, ops

def _postgres_using_alter_column(autogen_context: AutogenContext, op: ops.AlterColumnOp) -> str:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_postgres_using_to_text.py/add_postgres_using_to_alter_operation",
        "new_code": """
def add_postgres_using_to_alter_operation(op: ops.AlterColumnOp):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/add_postgres_using_to_text.py/add_postgres_using_to_text",
        "new_code": """
from alembic_postgresql_enum import UpgradeOps

def add_postgres_using_to_text(upgrade_ops: UpgradeOps):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/cast_old_array_enum_type_to_new",
        "new_code": """
from alembic_postgresql_enum import Connection, TableReference
from typing import List, Tuple

def cast_old_array_enum_type_to_new(connection: "Connection", table_reference: TableReference, enum_type_name: str, enum_values_to_rename: List[Tuple[str, str]]):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/cast_old_enum_type_to_new",
        "new_code": """
from alembic_postgresql_enum import Connection, TableReference
from typing import List, Tuple

def cast_old_enum_type_to_new(connection: "Connection", table_reference: TableReference, enum_type_name: str, enum_values_to_rename: List[Tuple[str, str]]):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/drop_type",
        "new_code": """
from alembic_postgresql_enum import Connection

def drop_type(connection: "Connection", schema: str, type_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/rename_type",
        "new_code": """
from alembic_postgresql_enum import Connection

def rename_type(connection: "Connection", schema: str, type_name: str, new_type_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/create_type",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import List

def create_type(connection: "Connection", schema: str, type_name: str, enum_values: List[str]):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/enum_type.py/get_all_enums",
        "new_code": """
from alembic_postgresql_enum import Connection

def get_all_enums(connection: "Connection", schema: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/column_default.py/get_column_default",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import Union

def get_column_default(connection: "Connection", table_schema: str, table_name: str, column_name: str) -> Union[str, None]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/column_default.py/drop_default",
        "new_code": """
from alembic_postgresql_enum import Connection

def drop_default(connection: "Connection", table_name_with_schema: str, column_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/column_default.py/set_default",
        "new_code": """
from alembic_postgresql_enum import Connection

def set_default(connection: "Connection", table_name_with_schema: str, column_name: str, default_value: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/column_default.py/rename_default_if_required",
        "new_code": """
from typing import List, Tuple

def rename_default_if_required(schema: str, default_value: str, enum_name: str, enum_values_to_rename: List[Tuple[str, str]]) -> str:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/column_default.py/_replace_strings_in_quotes",
        "new_code": """
from typing import List, Tuple

def _replace_strings_in_quotes(old_default: str, enum_values_to_rename: List[Tuple[str, str]]) -> str:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/comparison_operators.py/_create_comparison_operator",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import List, Tuple

def _create_comparison_operator(connection: "Connection", schema: str, enum_name: str, old_enum_name: str, enum_values_to_rename: List[Tuple[str, str]], operator: str, comparison_function_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/comparison_operators.py/create_comparison_operators",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import List, Tuple

def create_comparison_operators(connection: "Connection", schema: str, enum_name: str, old_enum_name: str, enum_values_to_rename: List[Tuple[str, str]]):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/comparison_operators.py/_drop_comparison_operator",
        "new_code": """
from alembic_postgresql_enum import Connection

def _drop_comparison_operator(connection: "Connection", schema: str, enum_name: str, old_enum_name: str, comparison_function_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/sql_commands/comparison_operators.py/drop_comparison_operators",
        "new_code": """
from alembic_postgresql_enum import Connection

def drop_comparison_operators(connection: "Connection", schema: str, enum_name: str, old_enum_name: str):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/types.py/ColumnType/__repr__",
        "new_code": """
class ColumnType:
    def __repr__(self):
        return f"ColumnType({self.name})"
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/types.py/TableReference/__repr__",
        "new_code": """
class TableReference:
    def __repr__(self):
        return f"TableReference({self.schema}, {self.table_name})"
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/types.py/TableReference/is_column_type_import_needed",
        "new_code": """
class TableReference:
    def is_column_type_import_needed(self):
        return True
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/types.py/TableReference/table_name_with_schema",
        "new_code": """
class TableReference:
    def table_name_with_schema(self):
        return f"{self.schema}.{self.table_name}"
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/defined_enums.py/_remove_schema_prefix",
        "new_code": """
def _remove_schema_prefix(enum_name: str, schema: str) -> str:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/defined_enums.py/get_defined_enums",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import Dict, List

def get_defined_enums(connection: "Connection", schema: str) -> Dict[str, List[str]]:
    defined_enums = {}
    for table in metadata.tables.values():
        for column in table.columns:
            if column_type_is_enum(column.type):
                enum_name = _remove_schema_prefix(column.type.name, schema)
                if enum_name not in defined_enums:
                    defined_enums[enum_name] = get_enum_values(column.type)
    return defined_enums
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/declared_enums.py/get_enum_values",
        "new_code": """
from sqlalchemy import Enum
from typing import Tuple

def get_enum_values(enum_type: Enum) -> Tuple[str, ...]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/declared_enums.py/column_type_is_enum",
        "new_code": """
def column_type_is_enum(column_type: Any) -> bool:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/declared_enums.py/get_declared_enums",
        "new_code": """
from typing import Union, List
from sqlalchemy import MetaData
from alembic_postgresql_enum import Connection, UpgradeOps

def get_declared_enums(metadata: Union[MetaData, List[MetaData]], schema: str, default_schema: str, connection: "Connection", upgrade_ops: Optional[UpgradeOps] = None) -> DeclaredEnumValues:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/get_default_from_alembic_ops.py/_get_default_from_add_column_op",
        "new_code": """
from alembic_postgresql_enum import AddColumnOp
from typing import Tuple

def _get_default_from_add_column_op(op: AddColumnOp, default_schema: str) -> Tuple[ColumnLocation, Optional[str]]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/get_default_from_alembic_ops.py/_get_default_from_alter_column_op",
        "new_code": """
from alembic_postgresql_enum import AlterColumnOp
from typing import Tuple

def _get_default_from_alter_column_op(op: AlterColumnOp, default_schema: str) -> Tuple[ColumnLocation, Optional[str]]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/get_default_from_alembic_ops.py/_get_default_from_column",
        "new_code": """
from sqlalchemy.sql.schema import Column
from typing import Tuple, Optional

def _get_default_from_column(column: Column, default_schema: str) -> Tuple[ColumnLocation, Optional[str]]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/get_enum_data/get_default_from_alembic_ops.py/get_just_added_defaults",
        "new_code": """
from typing import Dict, Optional
from alembic_postgresql_enum import UpgradeOps

def get_just_added_defaults(upgrade_ops: Optional[UpgradeOps], default_schema: str) -> Dict[ColumnLocation, Optional[str]]:
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/detection_of_changes/enum_creation.py/create_new_enums",
        "new_code": """
from alembic_postgresql_enum import EnumNamesToValues, UpgradeOps

def create_new_enums(defined_enums: EnumNamesToValues, declared_enums: EnumNamesToValues, schema: str, upgrade_ops: UpgradeOps):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/detection_of_changes/enum_alteration.py/sync_changed_enums",
        "new_code": """
from alembic_postgresql_enum import EnumNamesToValues, EnumNamesToTableReferences, UpgradeOps

def sync_changed_enums(defined_enums: EnumNamesToValues, declared_enums: EnumNamesToValues, table_references: EnumNamesToTableReferences, schema: str, upgrade_ops: UpgradeOps):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/detection_of_changes/enum_deletion.py/drop_unused_enums",
        "new_code": """
from alembic_postgresql_enum import EnumNamesToValues, UpgradeOps

def drop_unused_enums(defined_enums: EnumNamesToValues, declared_enums: EnumNamesToValues, schema: str, upgrade_ops: UpgradeOps):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/__init__",
        "new_code": """
from typing import List

class SyncEnumValuesOp:
    def __init__(self, schema: str, name: str, old_values: List[str], new_values: List[str], affected_columns: List[TableReference]):
        self.schema = schema
        self.name = name
        self.old_values = old_values
        self.new_values = new_values
        self.affected_columns = affected_columns
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/reverse",
        "new_code": """
class SyncEnumValuesOp:
    def reverse(self):
        return SyncEnumValuesOp(self.schema, self.name, self.new_values, self.old_values, self.affected_columns)
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/_set_enum_values",
        "new_code": """
from alembic_postgresql_enum import Connection
from typing import List, Tuple

class SyncEnumValuesOp:
    @classmethod
    def _set_enum_values(cls, connection: "Connection", enum_schema: str, enum_name: str, new_values: List[str], affected_columns: List[TableReference], enum_values_to_rename: List[Tuple[str, str]]):
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/sync_enum_values",
        "new_code": """
from typing import List, Tuple, Iterable

class SyncEnumValuesOp:
    @classmethod
    def sync_enum_values(cls, operations, enum_schema: str, enum_name: str, new_values: List[str], affected_columns: List[TableReference], enum_values_to_rename: Iterable[Tuple[str, str]] = tuple()):
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/to_diff_tuple",
        "new_code": """
from typing import Tuple, Any

class SyncEnumValuesOp:
    def to_diff_tuple(self) -> Tuple[Any, ...]:
        return (self.schema, self.name, self.old_values, self.new_values, self.affected_columns)
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/SyncEnumValuesOp/is_column_type_import_needed",
        "new_code": """
class SyncEnumValuesOp:
    def is_column_type_import_needed(self) -> bool:
        return any(column.is_column_type_import_needed() for column in self.affected_columns)
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/sync_enum_values.py/render_sync_enum_value_op",
        "new_code": """
from alembic_postgresql_enum import AutogenContext

def render_sync_enum_value_op(autogen_context: AutogenContext, op: SyncEnumValuesOp):
    autogen_context.imports.add("alembic_postgresql_enum.operations.sync_enum_values.SyncEnumValuesOp")
    autogen_context.imports.add("alembic_postgresql_enum.operations.sync_enum_values.render_sync_enum_value_op")
    return render_sync_enum_value_op(autogen_context, op)
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/enum_lifecycle_base.py/EnumLifecycleOp/__init__",
        "new_code": """
from typing import Iterable

class EnumLifecycleOp:
    def __init__(self, schema: str, name: str, enum_values: Iterable[str]):
        self.schema = schema
        self.name = name
        self.enum_values = enum_values
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/enum_lifecycle_base.py/EnumLifecycleOp/operation_name",
        "new_code": """
class EnumLifecycleOp:
    def operation_name(self) -> str:
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/enum_lifecycle_base.py/EnumLifecycleOp/to_diff_tuple",
        "new_code": """
from typing import Tuple, Any

class EnumLifecycleOp:
    def to_diff_tuple(self) -> Tuple[Any, ...]:
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/create_enum.py/CreateEnumOp/reverse",
        "new_code": """
class CreateEnumOp:
    def reverse(self):
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/create_enum.py/render_create_enum_op",
        "new_code": """
from alembic_postgresql_enum import AutogenContext

def render_create_enum_op(autogen_context: AutogenContext, op: CreateEnumOp):
    pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/drop_enum.py/DropEnumOp/reverse",
        "new_code": """
class DropEnumOp:
    def reverse(self):
        pass
        """
    },
    {
        "fqn_list": "alembic_postgresql_enum/operations/drop_enum.py/render_drop_enum_op",
        "new_code": """
from alembic_postgresql_enum import AutogenContext

def render_drop_enum_op(autogen_context: AutogenContext, op: DropEnumOp):
    pass
        """
    }
]

