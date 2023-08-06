# Copyright (C) OpenBII
# Team: CBICR
# SPDX-License-Identifier: Apache-2.0
# See: https://spdx.org/licenses/

import torch
from hnn.snn.neuron import Neuron
from hnn.snn.lif_recorder import LIFRecorder
from hnn.snn.lif import LIF, QLIF


class LIFNeuron(Neuron):
    '''含有Recorder的LIF神经元

    包含recorder和LIF神经元两部分, 需要重载record方法和_forward方法
    record方法用来记录神经元参数, _forward方法直接调用神经元的前向推理过程
    基类Neuron中的forward方法会自动调用record方法和_forward方法
    '''
    def __init__(self, T, v_th, v_leaky_alpha, v_leaky_beta, v_reset=0, v_leaky_adpt_en=False, v_init=None, window_size=1):
        Neuron.__init__(self, LIFRecorder, T)
        self.neuron = LIF(v_th=v_th, v_leaky_alpha=v_leaky_alpha, v_leaky_beta=v_leaky_beta, v_reset=v_reset,
                          v_leaky_adpt_en=v_leaky_adpt_en, v_init=v_init, window_size=window_size)

    def record(self, x: torch.Tensor):
        return self.recorder(
            x,
            self.neuron.if_node.fire.v_th,
            self.neuron.v_leaky.alpha,
            self.neuron.v_leaky.beta,
            self.neuron.if_node.reset.value,
            self.neuron.v_leaky.adpt_en,
            self.neuron.if_node.accumulate.v_init,
            self.T
        )


class QLIFNeuron(Neuron):
    '''支持量化的含有Recorder的LIF神经元
    '''
    def __init__(self, T, v_th, v_leaky_alpha, v_leaky_beta, v_reset=0, v_leaky_adpt_en=False, v_init=None, window_size=1):
        Neuron.__init__(self, LIFRecorder, T)
        self.neuron = QLIF(v_th=v_th, v_leaky_alpha=v_leaky_alpha, v_leaky_beta=v_leaky_beta, v_reset=v_reset,
                           v_leaky_adpt_en=v_leaky_adpt_en, v_init=v_init, window_size=window_size)

    def record(self, x: torch.Tensor):
        return self.recorder(
            x,
            self.neuron.if_node.fire.v_th,
            self.neuron.v_leaky.alpha,
            self.neuron.v_leaky.beta,
            self.neuron.if_node.reset.value,
            self.neuron.v_leaky.adpt_en,
            self.neuron.if_node.accumulate.v_init,
            self.T
        )