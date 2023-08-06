# -*- coding: utf-8 -*-
import onnxruntime


# 基于ONNX Runtime封装的通用ONNX推理器
class OnnxPredict(object):

    def __init__(self, model):
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        self.session = onnxruntime.InferenceSession(model, providers=providers)


    def predict(self, input_list):
        input_data = {}
        session_inputs = self.session.get_inputs()
        for i, data in enumerate(input_list):
            input_data[session_inputs[i].name] = data

        output_data = self.session.run(None, input_data)

        return output_data
