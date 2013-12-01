from codeop import CommandCompiler, Compile


class PyrCompile(Compile):
    pass


class PyrCompiler(CommandCompiler):
    def __init__(self, *args, **kwargs):
        CommandCompiler.__init__(self, *args, **kwargs)
        self.compiler = PyrCompile()
