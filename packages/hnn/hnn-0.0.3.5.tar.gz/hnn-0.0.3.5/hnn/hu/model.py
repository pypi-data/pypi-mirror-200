import torch
from hnn.hu.a2shu import A2SHU
from hnn.snn.model import Model


class A2SModel(torch.nn.Module):
    def __init__(self, T) -> None:
        super().__init__()
        self.T = T
        self.ann = None
        self.a2shu: A2SHU = None
        self.snn: Model = None
    
    def reshape(self, x: torch.Tensor):
        return x

    def forward(self, x, *args):
        x = self.ann(x)
        x = self.a2shu(x)  # [N, C, H, W] -> [N, C, H, W, T]
        x = self.reshape(x)  # [N, C, H, W, T] -> [T, ...]
        return self.snn.multi_step_forward(x, *args)