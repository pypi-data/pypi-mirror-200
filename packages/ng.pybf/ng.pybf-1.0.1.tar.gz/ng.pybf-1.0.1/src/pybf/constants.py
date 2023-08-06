from enum import Enum

Actions = Enum(
    "Actions", "INC_PTR DEC_PTR INC_VAL DEC_VAL OUTPUT INPUT LOOP_START LOOP_END"
)

TOKENS = {
    ">": Actions.INC_PTR,
    "<": Actions.DEC_PTR,
    "+": Actions.INC_VAL,
    "-": Actions.DEC_VAL,
    ".": Actions.OUTPUT,
    ",": Actions.INPUT,
    "[": Actions.LOOP_START,
    "]": Actions.LOOP_END,
}
