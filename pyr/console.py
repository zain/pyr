from code import InteractiveConsole
import readline, atexit, os, sys, pprint

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name

from pyr.compiler import PyrCompiler

# py3 compatibility
# raw_input renamed to input
try:
    input = raw_input
except NameError:
    pass
# new string types
try:
    basestring
    isstr = lambda s: isinstance(s, basestring)
except NameError:
    isstr = lambda s: isinstance(s, str)


def softspace(file, newvalue):
    oldvalue = 0
    try:
        oldvalue = file.softspace
    except AttributeError:
        pass
    try:
        file.softspace = newvalue
    except (AttributeError, TypeError):
        # "attribute-less object" or "read-only attributes"
        pass
    return oldvalue


class PyrConsole(InteractiveConsole):
    def __init__(self, locals=None, filename="<console>", histfile=None, pygments_style=None):
        InteractiveConsole.__init__(self, locals, filename)

        if not histfile:
            histfile = os.path.expanduser("~/.pyr_history")

        self.init_history(histfile)
        self.init_syntax_highlighting(pygments_style)
        self.init_pretty_printer()

        self.compile = PyrCompiler()

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

    def init_syntax_highlighting(self, pygments_style):
        self.past_lines = []

        if pygments_style:
            if isstr(pygments_style):
                self.pygments_style = get_style_by_name(pygments_style)
            else:
                self.pygments_style = pygments_style
        else:
            self.pygments_style = get_style_by_name('default')

        self.lexer = PythonLexer()
        self.formatter = Terminal256Formatter(style=self.pygments_style)

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
            pretty_line = highlight(line, self.lexer, self.formatter)
        else:
            self.past_lines.append(line)
            code_so_far = "\n".join(self.past_lines)
            pretty_code = highlight(code_so_far, self.lexer, self.formatter)

            if pretty_code[-1] == '\n':
                pretty_code = pretty_code[:-1]

            pretty_line = pretty_code.split('\n')[-1] + "\n"

        sys.stdout.write("\x1b[A")  # move up one line
        sys.stdout.write("\r\x1b[K")  # go to the start of the line
        sys.stdout.write(prompt)
        sys.stdout.write(pretty_line)
        sys.stdout.flush()

    def init_pretty_printer(self):
        self.pp = pprint.PrettyPrinter(indent=4)

    def pretty_print(self, result):
        if not result:
            return

        output = self.pp.pformat(result)

        if isstr(result):
            result = "'%s'" % result

        if self.pp.isreadable(result):
            output = highlight(output, self.lexer, self.formatter)
            sys.stdout.write(output)
        else:
            sys.stdout.write(output)
            sys.stdout.write("\n")

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            # do some special pretty printing if the source is an expression
            code = self.compile(source, filename, "eval")
            eval_expression = True
        except (OverflowError, SyntaxError, ValueError):
            eval_expression = False

        if eval_expression:
            if code is None:
                return True

            try:
                result = eval(code, self.locals)
                self.pretty_print(result)
            except SystemExit:
                raise
            except:
                self.showtraceback()
            else:
                if softspace(sys.stdout, 0):
                    print

            return False
        else:
            # fall back to default behavior
            return InteractiveConsole.runsource(self, source, filename, symbol)
