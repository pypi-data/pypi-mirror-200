import re
from ipykernel.ipkernel import IPythonKernel
from traitlets.config import LoggingConfigurable
from traitlets import TraitType, Unicode, Bool
from textwrap import dedent


class List(TraitType):

    default_value = None
    allow_none = True
    info_text = "a list that can be None"

    def validate(self, obj, value):
        if value is None or isinstance(value, list):
            return value
        self.error(obj, value)


class ExamKernel(IPythonKernel):
    implementation = "Exam"
    implementation_version = "0.1"
    language = "java"
    language_version = "3.6"
    language_info = {
        "name": "java",
        "mimetype": "text/x-java",
        "extension": ".java",
    }
    banner = "Exam kernel - Restricted kernel for exams"

    block_terminal_commands = Bool(
        default_value=True,
        help=dedent(
            """
            Whether to block all terminal commands or not.
            Default is blocked
        """
        ),
    ).tag(config=True)

    allowed_imports = List(
        default_value=None,
        help=dedent(
            """
            The imports that can be used.
            By default all imports are allowed
        """
        ),
    ).tag(config=True)

    blocked_imports = List(
        [],
        help=dedent(
            """
            The imports that are blocked.
            If allowed_imports is set this takes no effect."""
        ),
    ).tag(config=True)

    allowed_magics = List(
        None,
        help=dedent(
            """
            The magics that can be used.
            By default all magics are allowed."""
        ),
    ).tag(config=True)

    blocked_magics = List(
        None,
        help=dedent(
            """
            The magics that are blocked.
            If allowed_magics is set this takes no effect."""
        ),
    ).tag(config=True)

    init_code = Unicode(
        None,
        allow_none=True,
        help=dedent(
            """
            The code that should always be executed when the kernel is loaded.
        """
        ),
    ).tag(config=True)

    def __init__(self, **kwargs):
        super(ExamKernel, self).__init__(**kwargs)
        self.standard_import = re.compile(r"^\s*import\s+(\w+)", flags=re.MULTILINE)
        self.from_import = re.compile(r"^\s*from\s+(\w+)", flags=re.MULTILINE)
        self.cell_magic = re.compile(r"^\s*%%(\w+)", flags=re.MULTILINE)
        self.line_magic = re.compile(r"^\s*%(\w+)", flags=re.MULTILINE)
        self.blocked_imports.append("importlib")
        self.init_kernel()

    def init_kernel(self):
        """
        Execute the init_code at when the kernel is loaded
        """
        if self.init_code:
            super().do_execute(self.init_code, silent=False)

    def find_import(self, line: str) -> str:
        match = self.standard_import.match(line) or self.from_import.match(line)
        if match:
            return match.group(1).strip()

    def find_magic(self, line: str) -> str:
        match = self.cell_magic.match(line) or self.line_magic.match(line)
        if match:
            return match.group(1).strip()

    def remove_empty_lines(self, code: str) -> str:
        """
        Remove all empty lines at the beginning and end
        of the code snippet
        """
        return code.strip("\n")

    def remove_terminal_commands(self, code: str) -> str:
        """
        Remove all lines that start with an exclamation mark
        """
        if self.block_terminal_commands:
            return re.sub(r"^!.*", "", code, flags=re.MULTILINE)
        else:
            return code

    def blocked_import_message(self, lib, blocked=False):
        self.log.info(f"Creating blocked message with blocked={blocked} and lib={lib}")
        msg = f"No module named {lib} or {lib} blocked by kernel.\\n"
        if blocked:
            msg += f"The following imports are blocked: [{', '.join(self.blocked_imports)}]"
        else:
            msg += f"Allowed imports are: [{', '.join(self.allowed_imports)}]"
        return f"raise ModuleNotFoundError('{msg}')"

    def blocked_magic_message(self, magic, blocked=False):
        msg = f"No magic named {magic} or {magic} blocked by kernel.\\n"
        if blocked:
            msg += (
                f"The following magics are blocked: [{', '.join(self.blocked_magics)}]"
            )
        else:
            msg += f"Allowed magics are: [{', '.join(self.allowed_magics)}]"
        return f"raise ValueError('{msg}')"

    def sanitize_imports(self, code: str) -> str:

        if self.allowed_imports is None and len(self.blocked_imports) == 0:
            return code

        if self.allowed_imports is not None:
            sanitized = []
            for line in code.split("\n"):
                lib = self.find_import(line)
                if lib and lib not in self.allowed_imports:
                    line = self.blocked_import_message(lib)
                sanitized.append(line)
        else:
            sanitized = []
            for line in code.split("\n"):
                lib = self.find_import(line)
                if lib and lib in self.blocked_imports:
                    line = self.blocked_import_message(lib, blocked=True)
                sanitized.append(line)

        return "\n".join(sanitized)

    def sanitize_magics(self, code: str) -> str:

        if self.allowed_magics is None and self.blocked_magics is None:
            return code

        if self.allowed_magics is not None:
            sanitized = []
            for line in code.split("\n"):
                magic = self.find_magic(line)
                if magic and magic not in self.allowed_magics:
                    line = self.blocked_magic_message(magic)
                sanitized.append(line)
        else:
            sanitized = []
            for line in code.split("\n"):
                magic = self.find_magic(line)
                if magic and magic in self.blocked_magics:
                    line = self.blocked_magic_message(magic, blocked=True)
                sanitized.append(line)

        return "\n".join(sanitized)

    def sanitize(self, code: str) -> str:
        """
        Sanitize the code before executing it
        """
        code = self.remove_empty_lines(code)
        code = self.remove_terminal_commands(code)
        code = self.sanitize_magics(code)
        code = self.sanitize_imports(code)
        return code

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions: dict = None,
        allow_stdin: bool = False,
    ) -> dict:
        code = self.sanitize(code)
        return super().do_execute(
            code, silent, store_history, user_expressions, allow_stdin
        )
