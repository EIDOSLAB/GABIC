# Copyright 2020 InterDigital Communications, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from comp.models import SymmetricalTransFormer # full transformer
from comp.models import WACNN, WinGraph_WA  # channel-wise models

from .pretrained import load_pretrained as load_state_dict


models = {

    # Channel-Wise
    'wacnn_cw': WACNN, # Window-attention
    'stf': SymmetricalTransFormer, # Symmetric Transformer
    'wgrcnn_cw':WinGraph_WA
    
    
}
