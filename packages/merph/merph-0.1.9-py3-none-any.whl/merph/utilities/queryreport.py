from typing import List, Optional, Union

import pandas as pd
from prompt_toolkit import HTML, print_formatted_text, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator


def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            ret = True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            ret = False  # Terminal running IPython
        else:
            ret = False  # Other type (?)
        return ret
    except NameError:
        return False  # Probably standard Python interpreter


__ISNOTEBOOK = isnotebook()

style = Style.from_dict(
    {
        "title": "#3b76fe bold",
        "text": "#3b76fe",
        "query": "#33cc33",
        "query_ans": "#33cc33 italic",
        "error": "#ff0000",
        "fatal_error": "#ff0000 bold",
    }
)


def print_title(title_text: str) -> None:
    if __ISNOTEBOOK:
        print(title_text)
    else:
        print_formatted_text(
            HTML("<title>{}\n</title>".format(title_text)), style=style
        )


def print_text(text: str) -> None:
    if __ISNOTEBOOK:
        print(text)
    else:
        print_formatted_text(HTML("<text> {} </text>".format(text)), style=style)


def query_yes_no(question: str, default: str = "yes"):

    if default is None:
        ans = " [y/n] "
    elif default == "yes":
        ans = " [Y/n] "
    elif default == "no":
        ans = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if __ISNOTEBOOK:
        question_text = "{} {}:".format(question, ans)
        error_text = "Please respond with 'yes' or 'no' (or 'y' or 'n')"
    else:
        question_text = HTML(
            "<query> {} </query> <query_ans>".format(question)
            + "{}: </query_ans>".format(ans)
        )
        error_text = HTML(
            "<error> Please respond with 'yes' or 'no'" + "(or 'y' or 'n').\n </error>"
        )

    while True:
        if __ISNOTEBOOK:
            choice = input(question_text).lower()
        else:
            choice = prompt(question_text, style=style).lower()

        if default is not None and choice == "":
            return valid[default]
        if choice in valid:
            return valid[choice]

        if __ISNOTEBOOK:
            print(error_text)
        else:
            print_formatted_text(error_text, style=style)


def query_choices(
    question: str, choices: List[str] = ["y", "n"], default: Optional[str] = None
) -> bool:
    """Asks a question via input() with answer in choices.

    Args:
        question: a string that is presented to the user.
        choices: a list of allowed responses
        **default: Optional; the presumed answer if the user just hits <Enter>.

    Returns:
        The "answer" return value is True for "yes" or False for "no".
    """
    ans = "[" + "/".join(choices) + "]"
    if default is not None:
        ans += " (default {})".format(default)

    if __ISNOTEBOOK:
        question_text = "{} {}: ".format(question, ans)
        error_text = "Please respond with one of " + ",".join(choices) + "."
    else:
        question_text = HTML(
            "<query> {} </query> <query_ans>".format(question)
            + "{}: </query_ans>".format(ans)
        )
        error_text = HTML(
            "<error> Please respond with one of " + ",".join(choices) + ".\n </error>"
        )
        ans_completer = WordCompleter(choices)

    while True:
        if __ISNOTEBOOK:
            choice = input(question_text)
        else:
            choice = prompt(
                question_text,
                style=style,
                completer=ans_completer,
                complete_while_typing=True,
            )

        if default is not None and choice == "":
            return default
        if choice in choices:
            return choice
        if __ISNOTEBOOK:
            print(error_text)
        else:
            print_formatted_text(error_text, style=style)


def is_valid_float_str(text: str) -> bool:
    if text == "":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False


# def is_valid_float(num):
#     try:
#         float(num)
#         return True
#     except ValueError:
#         return False


def query_change_value(question: str, default: Optional[float] = None) -> float:
    """Ask a question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be a value

    Returns:
        float
    """

    if default is not None and not isinstance(default, float):
        raise ValueError(
            f"In query_change_value, default value {default} must be a float"
        )

    if default is None:
        ans = " "
    else:
        ans = f" [return for default = {default}] "

    if __ISNOTEBOOK:
        question_text = f"{question} {ans}:"
    else:
        validator = Validator.from_callable(
            is_valid_float_str,
            error_message="This input contains non-numeric characters",
            move_cursor_to_end=True,
        )
        question_text = HTML(
            f"<query> {question} </query> <query_ans> {ans}: </query_ans>"
        )

    while True:
        if __ISNOTEBOOK:
            choice = input(question_text)
        else:
            choice = prompt(question_text, style=style, validator=validator)

        if default is not None and choice == "":
            ret = default
        else:
            ret = float(choice)
        return ret


def query_set_value(question: str) -> float:
    """Ask a question via input() and return their answer.

    "question" is a string that is presented to the user.

    Returns:
        float
    """

    if __ISNOTEBOOK:
        question_text = f"{question} : "
    else:
        validator = Validator.from_callable(
            is_valid_float_str,
            error_message="This input contains non-numeric characters",
            move_cursor_to_end=True,
        )
        question_text = HTML(f"<query> {question} </query> : ")

    while True:
        if __ISNOTEBOOK:
            choice = input(question_text)
        else:
            choice = prompt(question_text, style=style, validator=validator)

        return float(choice)


def has_comma(text):
    text_split = text.split(",")
    if len(text_split) != 2:
        ret = False
    else:
        ret = True
    return ret
