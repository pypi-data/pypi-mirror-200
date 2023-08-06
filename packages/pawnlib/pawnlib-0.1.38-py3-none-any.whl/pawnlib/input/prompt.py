import json
import operator as _operator
from pawnlib.config import pawnlib_config as pawn, pconf
from pawnlib.typing import is_hex, is_int, is_float, FlatDict, Namespace, sys_exit, is_valid_token_address, is_valid_private_key
from InquirerPy import prompt, inquirer, get_style
from InquirerPy.validator import NumberValidator
from prompt_toolkit.validation import ValidationError, Validator, DynamicValidator
from prompt_toolkit.shortcuts import prompt as toolkit_prompt


class PromptWithArgument:
    def __init__(self, argument="", min_length=1, max_length=1000, **kwargs):
        self.argument = argument
        self._options = kwargs
        self.argument_name = ""
        self.argument_value = ""
        self.func_name = ""
        self.min_length = min_length
        self.max_length = max_length

    def _set_style(self, style_type='fuzzy'):
        if style_type == 'fuzzy':
            self._options['style'] = get_style(
                {
                    "question": "italic bold #ffffff",
                    # "questionmark": "#ffffff",
                    # "answer": "#000000",
                    "instruction": "italic bold #b6b8ba",
                    "answer": "#61afef bold",
                    "input": "#98c379 bold",
                    "fuzzy_info": "#474747",
                },
                style_override=False
            )
        elif style_type == 'prompt':
            self._options['style'] = {
                # "questionmark": "#ffffff",
                # "answer": "#000000",
                "answer": "#61afef bold",
                "question": "italic #ffffff bold",
                "input": "#98c379 bold",
                "long_instruction": "#96979A italic",
            }

    def _extract_option_to_variable(self, keys=None):
        for key in keys:
            if self._options.get(key):
                setattr(self, key, self._options.pop(key))

    def _parse_options(self, **options):
        _arg_missing_word = "DO_NOT_SET_THE_ARG"
        if options:
            self._options = options
        if not self._options:
            raise ValueError(f"Required argument, {self._options}")

        if self._options.get('message', _arg_missing_word) == _arg_missing_word and self._options.get('name'):
            self._options['message'] = f"Input {self._options.get('name').title()}"

        self._extract_option_to_variable(["min_length", "max_length", "argument", ])

        if _arg_missing_word == self.argument_value:
            raise ValueError(f"Cannot find argument in args. {self.argument}")
        _default_value = self._options.get('default')

        category_name = ""
        args_description = ""

        if is_data_args_namespace() and self.argument:
            _args = pawn.conf().data.args
            self.argument_name = self.argument
            self.argument_name_real = self.argument.replace("_", "-")
            self.argument_value = _args.__dict__.get(self.argument_name, _arg_missing_word)
            args_description =  f" ( --{self.argument_name_real} )"
            if getattr(_args, "subparser_name", None):
                category_name = f"[{_args.subparser_name.upper()}]"

        if not self._options.get('invalid_message', None) and not self._options.get('validate', None):
            self._options['validate'] = lambda result: len(result) > 1
            self._options['invalid_message'] = "minimum 1 selection"

        self._options['instruction'] = self._options.get('instruction', "") + args_description
        self._options['message'] = f"{category_name}{self._options.get('message','')}"

        if self.func_name == "prompt":
            if self._options.get('type', _arg_missing_word) == _arg_missing_word:
                self._options['type'] = "input"
            # else:
            #     if self._options['type'] == "list":
            #         self._options['type'] = "select"

            _options = dict(
                qmark="[❓]",
                amark="[❓]",
            )
            self._options.update(_options)

    def _prepare(self, **options):
        self._parse_options(**options)
        self._set_style()

    def _push_argument(self, result="", target_args=None):
        if is_data_args_namespace() and not target_args:
            target_args = pawn.conf().data.args
        if target_args and self.argument:
            setattr(target_args, self.argument, result)

    def _skip_if_value_in_args(self):
        if self.argument_value:
            return True

    def _decorator_common_executes(func):
        def executor(self, *args, **kwargs):
            pawn.console.debug(f"Starting executor - {func.__name__}")
            self.func_name = func.__name__
            self._prepare()

            if not self.argument_value or self.argument_value == "":
                result = func(self, *args, **kwargs)
                self._push_argument(result)
            else:
                self.argument_real_name = self.argument_name.replace("_", "-")
                pawn.console.debug(f"Skipped [yellow]{self._options.get('name','')}[/yellow] prompt, "
                                   f"Cause args value exists. --{self.argument_real_name}={self.argument_value}")
                self._check_force_validation(name=self.argument_real_name, value=self.argument_value)
                result = self._check_force_filtering(name=self.argument_real_name, value=self.argument_value)
            return result
        return executor

    def _check_force_validation(self, name=None, value=None):
        try:
            _validator = self._options.get('validate')
            if _validator:
                pawn.console.debug(f"force validation name={name} value={value}")
                if getattr(_validator, 'validate', None):
                    document = Namespace(**dict(text=value, cursor_position=name))
                    _validator.validate(document)
        except ValidationError as e:
            sys_exit(f"[bold]Failed to validate[/bold] : {e}")

    def _check_force_filtering(self, name=None, value=None):
        try:
            _filtering = self._options.get('filter')
            if _filtering:
                pawn.console.debug(f"force filtering name={name} value={value} return={_filtering(value)}")
                return _filtering(value)
        except ValidationError as e:
            sys_exit(f"[bold]Failed to filtering : {e}")
        return value

    def _remove_unnecessary_options(self, options):
        for opt in options:
            if self._options.get(opt, "__NOT_DEFINED__") != "__NOT_DEFINED__":
                del self._options[opt]

    @_decorator_common_executes
    def fuzzy(self, **kwargs):
        if kwargs:
            self._prepare(**kwargs)

        unnecessary_options = ["name", "type"]
        self._remove_unnecessary_options(unnecessary_options)

        if not self.argument_value:
            _prompt = inquirer.fuzzy(**self._options)
            input_value = _prompt.execute()
            # self._push_argument(result=input_value)
            return input_value
        else:
            pawn.console.debug(f"Skipped prompt, {self.argument_name}={self.argument_value}")
            return False

    @_decorator_common_executes
    def prompt(self, *args, **kwargs):
        pawn.console.log(f"executing prompt")
        _args_options_name = self._options.get('name', '')
        if args:
            answer = prompt(*args)
        else:
            style = None
            self._set_style(style_type="prompt")
            if self._options.get('style'):
                style = self._options.pop('style')
            answer = prompt(questions=self._options, style=style, style_override=False)
            if answer.get('name'):
                return answer['name']
            elif answer.get(_args_options_name, '__NOT_DEFINED__') != "__NOT_DEFINED__" :
                return answer[_args_options_name]
            elif len(answer) > 0:
                return answer[0]
            else:
                pawn.console.log(f"[red] Parse Error on prompt, answer={answer}")

    @_decorator_common_executes
    def checkbox(self):
        _default_options = dict(
            cycle=True,
            validate=lambda result: len(result) >= 1,
            invalid_message="should be at least 1 selection",
            instruction="(select at least 1)",
            enabled_symbol="✅",
            # disabled_symbol="⬜",
            disabled_symbol="◻️ ",
        )
        unnecessary_options = ["name", "type"]
        self._remove_unnecessary_options(unnecessary_options)

        self._options.update(_default_options)
        return inquirer.checkbox(**self._options).execute()


class CompareValidator(NumberValidator):
    def __init__(
            self,
            operator = "",
            length: int = 0,
            message: str = "Input should be a ",
            float_allowed: bool = False,
            value_type="number",
            min_value: int = 0,
            max_value: int = 0,

    ) -> None:
        super().__init__(message, float_allowed)
        self._message = f"{message} <{value_type.title()}> {operator}"
        if length:
            self._message = f"{self._message} {length}"
        self._float_allowed = float_allowed
        self._operator = operator
        self._length = length
        self._value_type = value_type

        self._min = min_value
        self._max = max_value

    def raise_error(self, document, message=""):
        _message = f"{self._message}, {message}"
        raise ValidationError(
            message=_message, cursor_position=document.cursor_position
        )

    def _numberify(self, value):
        if is_float(value) or is_int(value):
            if self._float_allowed:
                number = float(value)
            else:
                number = int(value)
        else:
            number = len(value)
        return number

    def _max_min_operator(self, value=0):
        if self._max > 0 and self._min > 0:
            if value > self._max or value < self._min:
                return False
            else:
                return True
        elif self._max > 0:
            if value > self._max:
                return False
        else:
            return True

    def validate(self, document) -> None:
        try:
            text_length = self._numberify(document.text)
            if self._value_type == "number":
                if not get_operator_truth(text_length, self._operator, self._length):
                    self.raise_error(document)
            elif self._value_type == "string":
                if not get_operator_truth(len(document.text), self._operator, self._length):
                    self.raise_error(document)
            elif self._value_type == "min_max":
                if self._max_min_operator(text_length):
                    return
                else:
                    self.raise_error(document, message=f"input_length={text_length}, min={self._min}, max={self._max}")

        except ValueError as e:
            self.raise_error(document, message=f"{e}")


class NumberCompareValidator(CompareValidator):
    def __init__(self, operator = "", length: int = 0, message: str = "Input should be a ", float_allowed: bool = False) -> None:
        super().__init__(operator=operator, length=length, message=message, float_allowed=float_allowed, value_type="number")


class StringCompareValidator(CompareValidator):
    def __init__(self, operator = "", length: int = 0, message: str = "Input should be a ", float_allowed: bool = False) -> None:
        super().__init__(operator=operator, length=length, message=message, float_allowed=float_allowed, value_type="string")


class MinMaxValidator(CompareValidator):
    def __init__(self, min_value: int = 0, max_value: int = 0, message: str = "Input should be a ", float_allowed: bool = False) -> None:
        super().__init__(min_value=min_value, max_value=max_value, message=message, float_allowed=float_allowed, value_type="min_max")


class PrivateKeyValidator(CompareValidator):
    def __init__(self, message: str = "Input should be a ", allow_none: bool = False) -> None:
        self.allow_none = allow_none
        super().__init__(message=message,  value_type="hex")

    def validate(self, document) -> None:
        try:
            text = document.text

            # if isinstance(text, str):
            if self.allow_none and not text:
                return
            elif not is_hex(text):
                self.raise_error(document, message=f"'{document.text}' is not Hex ")
            elif not is_valid_private_key(text):
                self.raise_error(document, message=f"Invalid Private Key, Length should be 64. len={len(text)}")
        except ValueError:
            self.raise_error(document)

def check_valid_private_length(text):
    private_length = 64
    if is_hex(text):
        if text.startswith("0x"):
            text = text[2:]
        if len(text) == private_length:
            return True
    return False


def get_operator_truth(inp, relate, cut):
    ops = {
        '>': _operator.gt,
        '<': _operator.lt,
        '>=': _operator.ge,
        '<=': _operator.le,
        '==': _operator.eq,
        '!=': _operator.ne,
        'include': lambda y, x: x in y,
        'exclude': lambda y, x: x not in y
    }
    return ops[relate](inp, cut)


def prompt_with_keyboard_interrupt(*args, **kwargs):
    answer = prompt(*args, **kwargs)
    if not answer:
        raise KeyboardInterrupt
    if isinstance(args[0], dict):
        arguments = args[0]
    else:
        arguments = args[0][0]
    if isinstance(answer, dict) and len(answer.keys()) == 1 and arguments and arguments.get('name'):
        return answer.get(arguments['name'])
    return answer


def inq_prompt(*args, **kwargs):
    if args:
        answer = prompt(*args)
    else:
        style = None
        if kwargs.get('style'):
            style = kwargs.pop('style')
        answer = prompt(questions=kwargs, style=style)
    if answer.get('name'):
        return answer['name']

    return answer[0]


def simple_input_prompt(
        name="", default="", type="input", choices=None,
        instruction=None, long_instruction=None, validate=None, filter=None, min_length=1, max_length=1000):

    if not name:
        raise ValueError("Required name for simple_input_prompt()" )

    if type == "list":
        _type_text = "select"
    else:
        _type_text = type

    if not name.isupper():
        name = name.title()

    _message = f"[{pawn.conf().data.args.subparser_name.upper()}] {_type_text.title()} {name}"
    _default_message = ""

    if default:
        _default_message = ""

    options = dict(
        message=f"{_message}{_default_message}?",
        type=type,
        default=str(default),
        # validate=lambda result: len(result) >= min_length,
        # validate=lambda result: min_length <= len(result) <= max_length,
        validate=MinMaxValidator(min_value=min_length, max_value=max_length),
        invalid_message=f"should be at least {min_length} , maximum {max_length}",
        instruction=instruction,
        qmark="[❓]",
        amark="[❓]",
        style={
            # "questionmark": "#ffffff",
            # "answer": "#000000",
            "answer": "#ffffff bold",
            "question": "#ffffff bold",
            "input": "#98c379 bold",
            "long_instruction": "#96979A italic",
        }
    )

    if isinstance(choices, list):
        options['choices'] = choices
        options['type'] = "list"

    if instruction:
        options['instruction'] = instruction


    if validate:
        options['validate'] = validate

    if filter:
        options['filter'] = filter

    if long_instruction:
        options['long_instruction'] = f"💡🤔 {long_instruction}"

    return inq_prompt(
        **options
    )


def change_select_pattern(items):
    result = []
    count = 0
    if isinstance(items, dict) or isinstance(items, FlatDict):
        for value, name in items.items():
            if name:
                name = f"{value} ({name})"
            else:
                name = value
            result.append({"name": f"{count:>2}) {name}", "value": value})
            count += 1
    else:
        return items
    return result


def tk_prompt(**kwargs):
    return toolkit_prompt(**kwargs)


def fuzzy_prompt(**kwargs):
    if not kwargs.get('style', None):
        kwargs['style'] = get_style(
            {
                "question": "bold #ffffff",
                # "questionmark": "#ffffff",
                # "answer": "#000000",
                "instruction": "italic bold #b6b8ba",
                "answer": "#61afef bold",
                "input": "#98c379 bold",
                "fuzzy_info": "#474747",
            },
            style_override=False
        )
    if not kwargs.get('invalid_message', None):
        kwargs['validate'] = lambda result: len(result) > 1
        kwargs['invalid_message'] = "minimum 1 selection"
    answer = inquirer.fuzzy(**kwargs).execute()
    return answer

def fuzzy_prompt_to_argument(**kwargs):
    _pconf = pconf()
    _arg_missing_word = "DO_NOT_SET_THE_ARG"
    if kwargs.get("argument"):
        argument = kwargs.pop("argument")
        _argument_name = argument.replace("_", "-")
        _argument_value = pawn.data.args.__dict__.get(_argument_name, _arg_missing_word)

        if _arg_missing_word == _argument_value:
            raise ValueError(f"Can not find argument in args. {argument}")
        _default_value = kwargs.get('default')

        kwargs['instruction'] = kwargs.get('instruction', "") + f"( --{_argument_name} {_default_value})"
        if not _argument_value and argument:
            response_value = fuzzy_prompt(**kwargs)
            setattr(_pconf.data.args, argument, response_value)
            return response_value
        else:
            pawn.console.debug("")
    else:
        raise ValueError(f"Required argument, {kwargs}")


def _check_undefined_dict_key(dict_item, key):
    if dict_item.get(key, '__NOT_DEFINED__KEY__') != '__NOT_DEFINED__KEY__':
        return True
    return False


def is_args_namespace():
    _pconf = pconf()
    if getattr(_pconf, "args", None):
        return True
    else:
        return False


def is_data_args_namespace():
    _pconf = pconf()
    if getattr(_pconf, "data", None) and getattr(_pconf.data, "args", None):
        return True
    else:
        return False

