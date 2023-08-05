from pysmi.mibinfo import MibInfo
from pysmi.codegen.base import AbstractCodeGen
from pysmi import debug

class NullCodeGen(AbstractCodeGen):
    """Dummy code generation backend.

       Could be used for disabling code generation at *MibCompiler*.
    """
    def genCode(self, ast, symbolTable, **kwargs):
        debug.logger & debug.flagCodegen and debug.logger('%s invoked' % self.__class__.__name__)
        return MibInfo(oid=None, name='', imported=[]), ''

    def genIndex(self, mibsMap, **kwargs):
        return ''
