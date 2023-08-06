from enum import Enum, auto
from typing import Optional


class Browsers(str, Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()


AssertionOperator = Enum(
    "AssertionOperator",
    {
        "equal": "==",
        "==": "==",
        "should be": "==",
        "inequal": "!=",
        "!=": "!=",
        "should not be": "!=",
        "less than": "<",
        "<": "<",
        "greater than": ">",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "contains": "*=",
        "not contains": "not contains",
        "*=": "*=",
        "starts": "^=",
        "^=": "^=",
        "should start with": "^=",
        "ends": "$=",
        "should end with": "$=",
        "$=": "$=",
        "matches": "$",
        "validate": "validate",
        "then": "then",
        "evaluate": "then",
    },
)
AssertionOperator.__doc__ = """
    Currently supported assertion operators are:
    |      = Operator =   |   = Alternative Operators =       |              = Description =                                                       | = Validate Equivalent =              |
    | ``==``              | ``equal``, ``should be``          | Checks if returned value is equal to expected value.                               | ``value == expected``                |
    | ``!=``              | ``inequal``, ``should not be``    | Checks if returned value is not equal to expected value.                           | ``value != expected``                |
    | ``>``               | ``greater than``                  | Checks if returned value is greater than expected value.                           | ``value > expected``                 |
    | ``>=``              |                                   | Checks if returned value is greater than or equal to expected value.               | ``value >= expected``                |
    | ``<``               | ``less than``                     | Checks if returned value is less than expected value.                              | ``value < expected``                 |
    | ``<=``              |                                   | Checks if returned value is less than or equal to expected value.                  | ``value <= expected``                |
    | ``*=``              | ``contains``                      | Checks if returned value contains expected value as substring.                     | ``expected in value``                |
    |                     | ``not contains``                  | Checks if returned value does not contain expected value as substring.             | ``expected in value``                |
    | ``^=``              | ``should start with``, ``starts`` | Checks if returned value starts with expected value.                               | ``re.search(f"^{expected}", value)`` |
    | ``$=``              | ``should end with``, ``ends``     | Checks if returned value ends with expected value.                                 | ``re.search(f"{expected}$", value)`` |
    | ``matches``         |                                   | Checks if given RegEx matches minimum once in returned value.                      | ``re.search(expected, value)``       |
    | ``validate``        |                                   | Checks if given Python expression evaluates to ``True``.                           |                                      |
    | ``evaluate``        |  ``then``                         | When using this operator, the keyword does return the evaluated Python expression. |                                      |
    Currently supported formatters for assertions are:
    |     = Formatter =     |                      = Description =                       |
    |  ``normalize spaces`` | Substitutes multiple spaces to single space from the value |
    |       ``strip``       | Removes spaces from the beginning and end of the value     |
    | ``apply to expected`` | Applies rules also for the expected value                  |
    Formatters are applied to the value before assertion is performed and keywords returns a value where rule is
    applied. Formatter is only applied to the value which keyword returns and not all rules are valid for all assertion
    operators. If ``apply to expected`` formatter is defined, then formatters are then formatter are also applied to
    expected value.
    """


def with_all_kinds(
    locator: str, /, pos_or_named, pos_or_named_def: bool = True, *, named_only: int = 0
):
    pass


def get_browsers(
    browsers: Browsers,
    assertion_operator: Optional[AssertionOperator] = None,
    assertion_expected: str = "",
):
    pass
