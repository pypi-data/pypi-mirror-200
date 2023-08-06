from inference_2 import ModelWrapper as Inference2ModelWrapper
from mop_utils.base_model_wrapper import BaseModelWrapper, InferenceInput, InferenceOutput
from typing import List, Dict



class ModelWrapper(Inference2ModelWrapper):
    def __init__(self) -> None:
        super().__init__()

    def init(self, model_root: str) -> None:
        super().init(model_root)

    def inference(self, item: Dict) -> Dict:
        print("logging in inference")

        return super().inference(item)

    def inference_batch(self, items: List[Dict]) -> List[Dict]:
        print(f'logging in inference batch')
        return super().inference_batch(items)




if __name__ == "__main__":
    model_wrapper = ModelWrapper()
    model_wrapper.init(model_root='../model')
    customized_input = {"data": "NIGGER PLEASE \n EAT A COCK, LOL HY."}
    c_output = model_wrapper.inference(customized_input)
    print(c_output)

    mop_input = InferenceInput(text="NIGGER PLEASE \n EAT A COCK, LOL HY.")
    customized_input = model_wrapper.convert_mop_input_to_model_input(mop_input)
    print(customized_input)

    mop_output = model_wrapper.convert_model_output_to_mop_output(c_output)
    print(mop_output)
