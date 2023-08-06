# -*- coding:utf-8 -*-
from openvino.runtime import Core


# 基于OpenVino推理引擎封装的通用OpenVino推理器
class OpenvinoPredict(object):
    def __init__(self, model, device='AUTO'):
        self.core = Core()
        self.model = self.core.read_model(model=model)
        self.compiled_model = self.core.compile_model(model=self.model, device_name=device)
        self.input_keys = self.compiled_model.inputs
        self.output_keys = self.compiled_model.outputs

    def predict(self, inputs: list) -> list:
        results = self.compiled_model(inputs)

        outputs = []
        for output_key in self.output_keys:
            outputs.append(results[output_key])

        return outputs
