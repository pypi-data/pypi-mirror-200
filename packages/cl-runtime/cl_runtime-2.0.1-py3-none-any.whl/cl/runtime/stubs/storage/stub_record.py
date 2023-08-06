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

from __future__ import annotations

from typing import Any, Dict, Optional

import cl.runtime as rt


class StubRecord(rt.Record):
    """Stub record used in tests."""

    primary_key_field_str: Optional[str]
    """First primary key attribute."""

    primary_key_field_int: Optional[int]
    """Second primary key attribute."""

    base_record_field_str: Optional[str]
    """String attribute of base class."""

    base_record_field_float: Optional[float]
    """Float attribute of base class."""

    def __init__(self):
        """Initialize instance attributes."""
        super().__init__()
        self.primary_key_field_str = None
        self.primary_key_field_int = None
        self.base_record_field_str = None
        self.base_record_field_float = None

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""
        return f'rt.stubs.StubRecord;{self.primary_key_field_str};{self.primary_key_field_int}'

    def to_dict(self) -> Dict[str, Any]:
        """Serialize self as dictionary (may return shallow copy)."""
        return {
            'primary_key_field_str': self.primary_key_field_str,
            'primary_key_field_int': self.primary_key_field_int,
            'base_record_field_str': self.base_record_field_str,
            'base_record_field_float': self.base_record_field_float,
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Populate self from dictionary (must perform deep copy)."""
        self.primary_key_field_str = data.get('primary_key_field_str')
        self.primary_key_field_int = data.get('primary_key_field_int')
        self.base_record_field_str = data.get('base_record_field_str')
        self.base_record_field_float = data.get('base_record_field_float')
        # TODO: detect extra fields in dict which are not in class and raise error

    @staticmethod
    def create(context: rt.Context) -> StubRecord:
        """Return an instance of this class populated with sample data."""

        obj = StubRecord()
        obj.context = context
        obj.primary_key_field_str = 'abc'
        obj.primary_key_field_int = 123
        obj.base_record_field_str = 'def'
        obj.base_record_field_float = 4.56
        obj.init()
        return obj
