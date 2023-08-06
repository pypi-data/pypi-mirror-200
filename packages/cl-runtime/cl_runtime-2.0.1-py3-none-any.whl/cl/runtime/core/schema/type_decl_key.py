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

from dataclasses import dataclass

from cl.runtime.core.storage.class_data import class_field
from cl.runtime.core.storage.class_record import ClassRecord


@dataclass
class TypeDeclKey(ClassRecord):
    """Key for the base class of type declaration in schema."""

    type_id: str = class_field()
    """
    Unique dot-delimited type identifier. May optionally include package alias.
    Used for table name in storage, and _type field in JSON.
    """

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""
        return f'rt.TypeDecl;{self.type_id}'
