from typing import Optional

from classiq.interface.generator.function_call import ZERO_INDICATOR, FunctionCall
from classiq.interface.generator.function_params import PortDirection


def _get_io_wire_name(name: str, call: FunctionCall, io: PortDirection) -> str:
    if io == PortDirection.Input:
        return f"{io.name}:{name}->{call.name}:{name}"
    else:
        return f"{call.name}:{name}->{io.name}:{name}"


def _get_wire_name(
    source_call: FunctionCall,
    source_pin_name: str,
    dest_pin_name: str,
    dest_call: Optional[FunctionCall],
) -> str:
    if dest_call is None:
        assert dest_pin_name == ZERO_INDICATOR
        return ZERO_INDICATOR
    return f"{source_call.name}:{source_pin_name}->{dest_call.name}:{dest_pin_name}"


def _set_model_output(call: FunctionCall, pin_name: str, wire_name: str):
    call_outputs = dict(call.outputs_dict)
    call_outputs[pin_name] = wire_name
    call.outputs = call_outputs
    if wire_name != ZERO_INDICATOR:
        call.non_zero_output_wires.append(wire_name)


def _set_model_input(call: Optional[FunctionCall], pin_name: str, wire_name: str):
    if call is None:
        return
    call_inputs = dict(call.inputs_dict)
    call_inputs[pin_name] = wire_name
    call.inputs = call_inputs
    call.non_zero_input_wires.append(wire_name)


def handle_inner_connection(
    source_call: FunctionCall,
    source_pin_name: str,
    dest_pin_name: str,
    dest_call: Optional[FunctionCall],
) -> None:
    wire_name = _get_wire_name(source_call, source_pin_name, dest_pin_name, dest_call)
    _set_model_output(source_call, source_pin_name, wire_name)
    _set_model_input(dest_call, dest_pin_name, wire_name)


def handle_io_connection(
    io_dir: PortDirection, call: FunctionCall, io_name: str
) -> str:
    wire_name = _get_io_wire_name(io_name, call, io_dir)
    if io_dir == PortDirection.Input:
        _set_model_input(call, io_name, wire_name)
    else:
        _set_model_output(call, io_name, wire_name)
    return wire_name
