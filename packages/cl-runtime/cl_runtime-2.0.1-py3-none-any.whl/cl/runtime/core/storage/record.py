# Copyright (C) 2023-present The CompatibL Runtime Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from cl.runtime import Context
from cl.runtime.core.storage.data import Data


class Record(Data):
    """
    Base class for database records that can be stored in a document DB,
    relational DB, key-value store, or filesystem.

    Derived classes must implement the following methods:

    * to_pk() - return type and primary key as semicolon-delimited string
    * to_dict() - serialize self as dictionary
    * from_dict(data_dict) - populate self from dictionary
    """

    context: Optional[Context]
    """
    Context provides platform-independent APIs for:

    * Databases and distributed cache
    * Logging and error reporting
    * Local or remote handler execution
    * Progress reporting
    * Virtualized filesystem
    """

    def __init__(self):
        """Initialize instance attributes."""
        self.context = None

    def init(self) -> None:
        """
        Update and validate object state after loading from DB and before saving to DB.

        Do nothing by default. Derived classes can override.
        """

    @abstractmethod
    def to_pk(self) -> str:
        """
        Return primary key (PK) as string.

        The key consists of database table name in dot-delimited format,
        followed by primary key attributes in semicolon-delimited format:

        simple_key = Type1;A;B

        For composite keys, the embedded keys are surrounded by curly braces.
        Helper method RecordUtil.composite_pk(...) is provided for generating
        such keys, and RecordUtil.split_composite_pk(...) for splitting them:

        composite_key = Type1;{Type2;A;B};C

        The first token of the key (i.e. Type1,2) is database table name.
        It can be customized as long as name collisions are avoided.
        """

    def __str__(self) -> str:
        """Return primary key (derived classes can override)."""
        return self.to_pk()
