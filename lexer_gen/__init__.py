'''

'''
from lexer_gen import *
from lexer_gen.utils import *
from typing import Any, Dict, Iterable, List, Set, Tuple, Union
from lexer_gen.ast import UnionNode, ConcatNode, ClosureNode, SymbolNode, EpsilonNode
from tools.pycompiler import Grammar
import pydot
import math


G = Grammar()

rgx = G.NonTerminal('rgx', True)
# T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
union_group, union, concat_group, concat, closure_group, closure, symbol_nt = G.NonTerminals('union_group union concat_group concat closure_group closure symbol_nt')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')


rgx %= union_group, lambda h,s: s[1]
union_group %= union + pipe + union_group, lambda h,s: UnionNode(s[1],s[3])
union_group %= union,lambda h,s: s[1]
union %= concat_group, lambda h,s: s[1]
concat_group %= concat + concat_group, lambda h,s: ConcatNode(s[1],s[2])
concat_group %= concat, lambda h,s: s[1]
concat %= closure_group, lambda h,s: s[1]
closure_group %= closure_group + star, lambda h,s: ClosureNode(s[1])
closure_group %= closure, lambda h,s: s[1]
closure %= symbol_nt, lambda h,s: s[1]
symbol_nt %= symbol, lambda h,s: SymbolNode(s[1])
symbol_nt %= epsilon, lambda h,s: EpsilonNode(s[1])
symbol_nt %= opar + rgx +cpar, lambda h,s: s[2]