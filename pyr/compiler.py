from codeop import CommandCompiler, Compile


class PyrCompile(Compile):
    def __call__(self, source, filename, symbol):
        return Compile.__call__(self, source, filename, symbol)


class PyrCompiler(CommandCompiler):
    def __init__(self, *args, **kwargs):
        CommandCompiler.__init__(self, *args, **kwargs)
        self.compiler = PyrCompile()
