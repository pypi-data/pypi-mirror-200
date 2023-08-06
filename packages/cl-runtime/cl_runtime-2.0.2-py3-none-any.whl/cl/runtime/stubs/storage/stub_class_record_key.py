# Copyright (C) 2023-present The Project Contributors
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

import cl.runtime as rt


@dataclass
class StubClassRecordKey(rt.ClassRecord):
    """Stub dataclass-based record sample used in tests."""

    primary_key_field_str: str = rt.class_field()
    """First primary key attribute."""

    primary_key_field_int: int = rt.class_field()
    """Second primary key attribute."""

    def to_pk(self) -> str:
        """Return primary key (PK) as string."""
        return f'rt.stubs.StubClassRecord;{self.primary_key_field_str};{self.primary_key_field_int}'
