# -*- coding: utf-8 -*-
"""
Author  : NextPCG
"""

from inspect import signature, Signature
from functools import wraps
from typing import *
from .field import Field, FieldCategory
import json
from .const import *
import logging
from .dson import DsonMetaInfo


def create_dson_from_pda(func: Callable, tag, dson_meta_info: DsonMetaInfo) -> Dict:
    cda_json = {}
    try:
        func_sig = signature(func)
        func_name = func.__name__
        inputs, params = get_inputs(func_sig)
        outputs = get_outputs(func_sig)
        cda_json_cda = {dson_inputs_tag: inputs, dson_params_tag: params, dson_outputs_tag: outputs, dson_meta_field_tag: dson_meta_info.to_json()}
        cda_json = {func_name + "." + tag: cda_json_cda}
    except Exception as e:
        logging.exception(e)
    finally:
        return cda_json


def get_inputs(sig: Signature):
    inputs = {}
    params = {}
    input_index = 0
    for param in sig.parameters.values():
        if param.default is param.empty:
            # no default value, we put it in inputs
            param_type = param.annotation
            assert issubclass(param_type, Field)
            field = param_type.create_json_field(FieldCategory.Input, param.name)
            input_index += 1
            inputs[dson_input_tag + str(input_index)] = field
        else:
            # have default value, we put it in params
            param_type = param.annotation
            field = param_type.create_json_field(FieldCategory.Param, param.name)
            if not param_type.support_param:
                raise Exception(str(param_type) + " can't be param")
            # param_value = param_type(param.default)
            # param_value.get_output(field, "Default Value")
            param_type.get_param_default(field, param.default)
            params[param.name] = field
    return inputs, params


def get_outputs(sig: Signature):
    outputs = {}
    return_annotation = sig.return_annotation
    output_index = 0
    if return_annotation is None:
        return outputs
    if hasattr(return_annotation, '__origin__') and (return_annotation.__origin__ == tuple or return_annotation.__origin__ == Tuple):
        for ele_type in return_annotation.__args__:
            output_index += 1
            outputs["output" + str(output_index)] = ele_type.create_json_field(FieldCategory.Output)
    else:
        output_index += 1
        outputs['output' + str(output_index)] = return_annotation.create_json_field(FieldCategory.Output)
    return outputs


# for test
if __name__ == "__main__":
    from field import Int, Int2, String, ListField


    def foo(a: Int, b: ListField[Int2] = [1, 2], c: Int2 = (1, 2)) -> String:
        pass


    jj = create_dson_from_pda(foo)
    file_path = "test.json"
    with open(file_path, "w") as fp:
        json.dump(jj, fp)
