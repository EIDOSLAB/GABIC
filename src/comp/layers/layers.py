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



import torch
import torch.nn as nn
from .win_attention import WinBasedAttention
from comp.gcn_lib.local_graph_pyg import WindowGrapherPyg

__all__ = [
    "conv3x3",
    "subpel_conv3x3",
    "conv1x1",
    "Win_noShift_Attention",

    "Win_GraphPyg",

]


def conv3x3(in_ch: int, out_ch: int, stride: int = 1) -> nn.Module:
    """3x3 convolution with padding."""
    return nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=stride, padding=1)


def subpel_conv3x3(in_ch: int, out_ch: int, r: int = 1) -> nn.Sequential:
    """3x3 sub-pixel convolution for up-sampling."""
    return nn.Sequential(
        nn.Conv2d(in_ch, out_ch * r ** 2, kernel_size=3, padding=1), nn.PixelShuffle(r)
    )


def conv1x1(in_ch: int, out_ch: int, stride: int = 1) -> nn.Module:
    """1x1 convolution."""
    return nn.Conv2d(in_ch, out_ch, kernel_size=1, stride=stride)


class ResidualUnit(nn.Module):
    """Simple residual unit."""

    def __init__(self, dim):

        super().__init__()
        self.conv = nn.Sequential(
            conv1x1(dim, dim // 2),
            nn.GELU(),
            conv3x3(dim // 2, dim // 2),
            nn.GELU(),
            conv1x1(dim // 2, dim),
        )
        self.relu = nn.GELU()

    def forward(self, x):
        identity = x
        out = self.conv(x)
        out += identity
        out = self.relu(out)
        return out

class Win_noShift_Attention(nn.Module):
    """Window-based self-attention module."""

    def __init__(self, dim, num_heads=8, window_size=8, shift_size=0):
        super().__init__()
        N = dim

        self.conv_a = nn.Sequential(ResidualUnit(N), ResidualUnit(N), ResidualUnit(N))

        self.conv_b = nn.Sequential(
            WinBasedAttention(dim=dim, num_heads=num_heads, window_size=window_size, shift_size=shift_size),
            ResidualUnit(N),
            ResidualUnit(N),
            ResidualUnit(N),
            conv1x1(N, N),
        )

    def forward(self, x):
        identity = x
        a = self.conv_a(x)
        b = self.conv_b(x)
        out = a * torch.sigmoid(b)
        out += identity
        return out
    

    
class Win_GraphPyg(nn.Module):
    """Window-based graph pyg module."""

    def __init__(self, dim, window_size=8, knn = 9, conv = 'transf', heads = 8, use_edge_attr = False, dissimilarity = False):
        super().__init__()
        N = dim

        self.conv_a = nn.Sequential(ResidualUnit(N), ResidualUnit(N), ResidualUnit(N))

        self.conv_b = nn.Sequential(
            WindowGrapherPyg(dim=dim, window_size=window_size, knn=knn,conv=conv, heads=heads, use_edge_attr=use_edge_attr, dissimilarity=dissimilarity),
            ResidualUnit(N),
            ResidualUnit(N),
            ResidualUnit(N),
            conv1x1(N, N),
        )

    def forward(self, x):
        identity = x
        a = self.conv_a(x)
        b = self.conv_b(x)
        out = a * torch.sigmoid(b)
        out += identity
        return out
