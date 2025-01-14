# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

import pytest

from airflow.providers.microsoft.azure.utils import get_field


def test_get_field_warns_on_dupe():
    with pytest.warns(UserWarning, match="Using value for `this_param`"):
        value = get_field(
            conn_id="my_conn",
            conn_type="this_type",
            extras=dict(extra__this_type__this_param="prefixed", this_param="non-prefixed"),
            field_name="this_param",
        )
    assert value == "non-prefixed"


@pytest.mark.parametrize(
    "input, expected",
    [
        (dict(this_param="non-prefixed"), "non-prefixed"),
        (dict(this_param=None), None),
        (dict(extra__this_type__this_param="prefixed"), "prefixed"),
        (dict(extra__this_type__this_param=""), None),
        (dict(extra__this_type__this_param=None), None),
        (dict(extra__this_type__this_param="prefixed", this_param="non-prefixed"), "non-prefixed"),
        (dict(extra__this_type__this_param="prefixed", this_param=""), None),
        (dict(extra__this_type__this_param="prefixed", this_param=0), 0),
        (dict(extra__this_type__this_param="prefixed", this_param=False), False),
        (dict(extra__this_type__this_param="prefixed", this_param=" "), " "),
    ],
)
def test_get_field_non_prefixed(input, expected):
    value = get_field(
        conn_id="my_conn",
        conn_type="this_type",
        extras=input,
        field_name="this_param",
    )
    assert value == expected
