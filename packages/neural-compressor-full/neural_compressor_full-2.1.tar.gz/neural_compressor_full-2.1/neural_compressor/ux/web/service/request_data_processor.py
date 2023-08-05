# -*- coding: utf-8 -*-
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Request data processor."""

from typing import Any, Dict

from neural_compressor.ux.utils.exceptions import ClientErrorException


class RequestDataProcessor:
    """Request data processor."""

    @staticmethod
    def get_string_value(data: Dict[str, Any], name: str) -> str:
        """Get string value from request."""
        try:
            return data[name][0]
        except KeyError:
            raise ClientErrorException(f"Missing {name} parameter")
