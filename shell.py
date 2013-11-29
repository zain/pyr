from code import InteractiveConsole
import readline, atexit, os, sys

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter

# py3 compatibility; raw_input renamed to input
try:
    input = raw_input
except NameError:
    pass


class PyrConsole(InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        InteractiveConsole.__init__(self, locals, filename)
        self.init_history(histfile)
        self.init_syntax_highlighting()

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

    def init_syntax_highlighting(self):
        self.past_lines = []

    def raw_input(self, prompt=""):
        line = input(prompt)
        self.syntax_highlight(line, prompt)
        return line

    def syntax_highlight(self, line, prompt):
        if not line.strip():
            return

        is_first_line = (prompt == sys.ps1)
        if is_first_line:
            self.past_lines = [line]
            pretty_line = highlight(line, PythonLexer(), Terminal256Formatter())
        else:
            self.past_lines.append(line)
            code_so_far = "\n".join(self.past_lines)
            pretty_code = highlight(code_so_far, PythonLexer(), Terminal256Formatter())

            if pretty_code[-1] == '\n':
                pretty_code = pretty_code[:-1]

            pretty_line = pretty_code.split('\n')[-1] + "\n"

        sys.stdout.write("\x1b[A")  # move up one line
        sys.stdout.write("\r\x1b[K")  # go to the start of the line
        sys.stdout.write(prompt)
        sys.stdout.write(pretty_line)
        sys.stdout.flush()


console = PyrConsole()
console.interact()
