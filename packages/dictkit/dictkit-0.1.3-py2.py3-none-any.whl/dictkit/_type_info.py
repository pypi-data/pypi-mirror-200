import typing
import types
import collections
import abc
import contextlib
import re

TypeInfo = collections.namedtuple("TypeInfo", ["cls", "type", "origin", "has_args", "cls_is_type", "kind", "type_when_params", "th_1", "th_2", "th_3"])


type_data = {
    'None': TypeInfo(None, types.NoneType, None, False, False, 'builtin', False, False, False, False),
    'ByteString': TypeInfo(typing.ByteString, typing._SpecialGenericAlias, collections.abc.ByteString, False, False, 'typing', False, False, False, False),  # type:ignore
    'Hashable': TypeInfo(typing.Hashable, typing._SpecialGenericAlias, collections.abc.Hashable, False, False, 'typing', False, False, False, False),  # type:ignore
    'Sized': TypeInfo(typing.Sized, typing._SpecialGenericAlias, collections.abc.Sized, False, False, 'typing', False, False, False, False),  # type:ignore
    'str': TypeInfo(str, type, None, False, True, 'builtin', False, False, False, False),
    'int': TypeInfo(int, type, None, False, True, 'builtin', False, False, False, False),
    'float': TypeInfo(float, type, None, False, True, 'builtin', False, False, False, False),
    'complex': TypeInfo(complex, type, None, False, True, 'builtin', False, False, False, False),
    'range': TypeInfo(range, type, None, False, True, 'builtin', False, False, False, False),
    'bool': TypeInfo(bool, type, None, False, True, 'builtin', False, False, False, False),
    'bytes': TypeInfo(bytes, type, None, False, True, 'builtin', False, False, False, False),
    'bytearray': TypeInfo(bytearray, type, None, False, True, 'builtin', False, False, False, False),
    'memoryview': TypeInfo(memoryview, type, None, False, True, 'builtin', False, False, False, False),
    'NoneType': TypeInfo(types.NoneType, type, None, False, True, 'types', False, False, False, False),
    'GenericAlias': TypeInfo(types.GenericAlias, type, None, True, True, 'types', False, False, False, False),
    'MethodDescriptorType': TypeInfo(types.MethodDescriptorType, type, None, False, True, 'types', False, False, False, False),
    'MethodWrapperType': TypeInfo(types.MethodWrapperType, type, None, False, True, 'types', False, False, False, False),
    'WrapperDescriptorType': TypeInfo(types.WrapperDescriptorType, type, None, False, True, 'types', False, False, False, False),
    'BuiltinFunctionType': TypeInfo(types.BuiltinFunctionType, type, None, False, True, 'types', False, False, False, False),
    'BuiltinMethodType': TypeInfo(types.BuiltinMethodType, type, None, False, True, 'types', False, False, False, False),
    'CellType': TypeInfo(types.CellType, type, None, False, True, 'types', False, False, False, False),
    'ClassMethodDescriptorType': TypeInfo(types.ClassMethodDescriptorType, type, None, False, True, 'types', False, False, False, False),
    'CodeType': TypeInfo(types.CodeType, type, None, False, True, 'types', False, False, False, False),
    'CoroutineType': TypeInfo(types.CoroutineType, type, None, False, True, 'types', False, False, False, False),
    'DynamicClassAttribute': TypeInfo(types.DynamicClassAttribute, type, None, False, True, 'types', False, False, False, False),
    'EllipsisType': TypeInfo(types.EllipsisType, type, None, False, True, 'types', False, False, False, False),
    'FrameType': TypeInfo(types.FrameType, type, None, False, True, 'types', False, False, False, False),
    'FunctionType': TypeInfo(types.FunctionType, type, None, False, True, 'types', False, False, False, False),
    'GeneratorType': TypeInfo(types.GeneratorType, type, None, False, True, 'types', False, False, False, False),
    'GetSetDescriptorType': TypeInfo(types.GetSetDescriptorType, type, None, False, True, 'types', False, False, False, False),
    'LambdaType': TypeInfo(types.LambdaType, type, None, False, True, 'types', False, False, False, False),
    'MemberDescriptorType': TypeInfo(types.MemberDescriptorType, type, None, False, True, 'types', False, False, False, False),
    'MethodType': TypeInfo(types.MethodType, type, None, False, True, 'types', False, False, False, False),
    'ModuleType': TypeInfo(types.ModuleType, type, None, False, True, 'types', False, False, False, False),
    'NotImplementedType': TypeInfo(types.NotImplementedType, type, None, False, True, 'types', False, False, False, False),
    'SimpleNamespace': TypeInfo(types.SimpleNamespace, type, None, False, True, 'types', False, False, False, False),
    'TracebackType': TypeInfo(types.TracebackType, type, None, False, True, 'types', False, False, False, False),
    'UnionType': TypeInfo(types.UnionType, type, None, True, True, 'types', False, False, False, False),
    '_GeneratorWrapper': TypeInfo(types._GeneratorWrapper, type, None, False, True, 'types', False, False, False, False),  # type:ignore
    'ABCMeta': TypeInfo(abc.ABCMeta, type, None, False, True, 'typing', False, False, False, False),
    'Any': TypeInfo(typing.Any, typing._AnyMeta, None, False, True, 'typing', False, False, False, False),  # type:ignore
    'BinaryIO': TypeInfo(typing.BinaryIO, type, None, False, True, 'typing', False, False, False, False),
    'ForwardRef': TypeInfo(typing.ForwardRef, type, None, False, True, 'typing', False, False, False, False),
    'Generic': TypeInfo(typing.Generic, type, typing.Generic, False, True, 'typing', False, False, False, False),
    'NamedTupleMeta': TypeInfo(typing.NamedTupleMeta, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    'NewType': TypeInfo(typing.NewType, type, None, False, True, 'typing', False, False, False, False),
    'ParamSpec': TypeInfo(typing.ParamSpec, type, None, False, True, 'typing', False, False, False, False),
    'ParamSpecArgs': TypeInfo(typing.ParamSpecArgs, type, None, False, True, 'typing', False, False, False, False),
    'ParamSpecKwargs': TypeInfo(typing.ParamSpecKwargs, type, None, False, True, 'typing', False, False, False, False),
    'Protocol': TypeInfo(typing.Protocol, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'SupportsBytes': TypeInfo(typing.SupportsBytes, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'SupportsComplex': TypeInfo(typing.SupportsComplex, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'SupportsFloat': TypeInfo(typing.SupportsFloat, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'SupportsIndex': TypeInfo(typing.SupportsIndex, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'SupportsInt': TypeInfo(typing.SupportsInt, typing._ProtocolMeta, None, False, True, 'typing', False, False, False, False),
    'Text': TypeInfo(str, type, None, False, True, 'typing', False, False, False, False),
    'TextIO': TypeInfo(typing.TextIO, type, None, False, True, 'typing', False, False, False, False),
    'TypeVar': TypeInfo(typing.TypeVar, type, None, False, True, 'typing', False, False, False, False),
    'TypeVarTuple': TypeInfo(typing.TypeVarTuple, type, None, False, True, 'typing', False, False, False, False),
    '_AnnotatedAlias': TypeInfo(typing._AnnotatedAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_AnyMeta': TypeInfo(typing._AnyMeta, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_BaseGenericAlias': TypeInfo(typing._BaseGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_BoundVarianceMixin': TypeInfo(typing._BoundVarianceMixin, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_CallableGenericAlias': TypeInfo(typing._CallableGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_CallableType': TypeInfo(typing._CallableType, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_ConcatenateGenericAlias': TypeInfo(typing._ConcatenateGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_DeprecatedType': TypeInfo(typing._DeprecatedType, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_Final': TypeInfo(typing._Final, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_GenericAlias': TypeInfo(typing._GenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_Immutable': TypeInfo(typing._Immutable, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_LiteralGenericAlias': TypeInfo(typing._LiteralGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_LiteralSpecialForm': TypeInfo(typing._LiteralSpecialForm, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_NamedTuple': TypeInfo(typing.NamedTuple, typing.NamedTupleMeta, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_NotIterable': TypeInfo(typing._NotIterable, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_PickleUsingNameMixin': TypeInfo(typing._PickleUsingNameMixin, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_ProtocolMeta': TypeInfo(typing._ProtocolMeta, type, None, False, True, 'typing', False, False, False, False),
    '_SpecialForm': TypeInfo(typing._SpecialForm, type, None, False, True, 'typing', False, False, False, False),
    '_SpecialGenericAlias': TypeInfo(typing._SpecialGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_TupleType': TypeInfo(typing._TupleType, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_TypedDict': TypeInfo(typing.TypedDict, typing._TypedDictMeta, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_TypedDictMeta': TypeInfo(typing._TypedDictMeta, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_TypingEllipsis': TypeInfo(typing._TypingEllipsis, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_UnionGenericAlias': TypeInfo(typing._UnionGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_UnpackGenericAlias': TypeInfo(typing._UnpackGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    '_alias': TypeInfo(typing._SpecialGenericAlias, type, None, False, True, 'typing', False, False, False, False),  # type:ignore
    'Coroutine': TypeInfo(typing.Coroutine, typing._SpecialGenericAlias, collections.abc.Coroutine, False, False, 'typing', typing._GenericAlias, False, False, True),  # type:ignore
    'Generator': TypeInfo(typing.Generator, typing._SpecialGenericAlias, collections.abc.Generator, False, False, 'typing', typing._GenericAlias, False, False, True),  # type:ignore
    'Callable': TypeInfo(typing.Callable, typing._CallableType, collections.abc.Callable, False, False, 'typing', typing._CallableGenericAlias, False, True, False),  # type:ignore
    'AsyncGenerator': TypeInfo(typing.AsyncGenerator, typing._SpecialGenericAlias, collections.abc.AsyncGenerator, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'ChainMap': TypeInfo(typing.ChainMap, typing._SpecialGenericAlias, collections.ChainMap, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'DefaultDict': TypeInfo(typing.DefaultDict, typing._SpecialGenericAlias, collections.defaultdict, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'Dict': TypeInfo(typing.Dict, typing._SpecialGenericAlias, dict, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'ItemsView': TypeInfo(typing.ItemsView, typing._SpecialGenericAlias, collections.abc.ItemsView, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'Mapping': TypeInfo(typing.Mapping, typing._SpecialGenericAlias, collections.abc.Mapping, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'MutableMapping': TypeInfo(typing.MutableMapping, typing._SpecialGenericAlias, collections.abc.MutableMapping, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'OrderedDict': TypeInfo(typing.OrderedDict, typing._SpecialGenericAlias, collections.OrderedDict, False, False, 'typing', typing._GenericAlias, False, True, False),  # type:ignore
    'Annotated': TypeInfo(typing.Annotated, type, None, False, True, 'typing', typing._AnnotatedAlias, False, True, True),  # type:ignore
    'AbstractSet': TypeInfo(typing.AbstractSet, typing._SpecialGenericAlias, collections.abc.Set, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'AsyncContextManager': TypeInfo(typing.AsyncContextManager, typing._SpecialGenericAlias, contextlib.AbstractAsyncContextManager, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'AsyncIterable': TypeInfo(typing.AsyncIterable, typing._SpecialGenericAlias, collections.abc.AsyncIterable, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'AsyncIterator': TypeInfo(typing.AsyncIterator, typing._SpecialGenericAlias, collections.abc.AsyncIterator, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Awaitable': TypeInfo(typing.Awaitable, typing._SpecialGenericAlias, collections.abc.Awaitable, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Collection': TypeInfo(typing.Collection, typing._SpecialGenericAlias, collections.abc.Collection, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Container': TypeInfo(typing.Container, typing._SpecialGenericAlias, collections.abc.Container, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'ContextManager': TypeInfo(typing.ContextManager, typing._SpecialGenericAlias, contextlib.AbstractContextManager, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Counter': TypeInfo(typing.Counter, typing._SpecialGenericAlias, collections.Counter, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Deque': TypeInfo(typing.Deque, typing._SpecialGenericAlias, collections.deque, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'FrozenSet': TypeInfo(typing.FrozenSet, typing._SpecialGenericAlias, frozenset, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Iterable': TypeInfo(typing.Iterable, typing._SpecialGenericAlias, collections.abc.Iterable, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Iterator': TypeInfo(typing.Iterator, typing._SpecialGenericAlias, collections.abc.Iterator, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'KeysView': TypeInfo(typing.KeysView, typing._SpecialGenericAlias, collections.abc.KeysView, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'List': TypeInfo(typing.List, typing._SpecialGenericAlias, list, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'MappingView': TypeInfo(typing.MappingView, typing._SpecialGenericAlias, collections.abc.MappingView, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Match': TypeInfo(typing.Match, typing._SpecialGenericAlias, re.Match, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'MutableSequence': TypeInfo(typing.MutableSequence, typing._SpecialGenericAlias, collections.abc.MutableSequence, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'MutableSet': TypeInfo(typing.MutableSet, typing._SpecialGenericAlias, collections.abc.MutableSet, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Pattern': TypeInfo(typing.Pattern, typing._SpecialGenericAlias, re.Pattern, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Reversible': TypeInfo(typing.Reversible, typing._SpecialGenericAlias, collections.abc.Reversible, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Sequence': TypeInfo(typing.Sequence, typing._SpecialGenericAlias, collections.abc.Sequence, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Set': TypeInfo(typing.Set, typing._SpecialGenericAlias, set, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Type': TypeInfo(typing.Type, typing._SpecialGenericAlias, type, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'ValuesView': TypeInfo(typing.ValuesView, typing._SpecialGenericAlias, collections.abc.ValuesView, False, False, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'IO': TypeInfo(typing.IO, type, None, False, True, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'SupportsAbs': TypeInfo(typing.SupportsAbs, typing._ProtocolMeta, None, False, True, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'SupportsRound': TypeInfo(typing.SupportsRound, typing._ProtocolMeta, None, False, True, 'typing', typing._GenericAlias, True, False, False),  # type:ignore
    'Tuple': TypeInfo(typing.Tuple, typing._TupleType, tuple, False, False, 'typing', typing._GenericAlias, True, True, True),  # type:ignore
    'list': TypeInfo(list, type, None, False, True, 'builtin', types.GenericAlias, True, True, True),
    'tuple': TypeInfo(tuple, type, None, False, True, 'builtin', types.GenericAlias, True, True, True),
    'dict': TypeInfo(dict, type, None, False, True, 'builtin', types.GenericAlias, True, True, True),
    'set': TypeInfo(set, type, None, False, True, 'builtin', types.GenericAlias, True, True, True),
    'frozenset': TypeInfo(frozenset, type, None, False, True, 'builtin', types.GenericAlias, True, True, True),
    'AsyncGeneratorType': TypeInfo(types.AsyncGeneratorType, type, None, False, True, 'types', types.GenericAlias, True, True, True),
    'MappingProxyType': TypeInfo(types.MappingProxyType, type, None, False, True, 'types', types.GenericAlias, True, True, True),
    'defaultdict': TypeInfo(collections.defaultdict, type, None, False, True, 'typing', types.GenericAlias, True, True, True),
}

























"""
                                                     cls_name                    type_name                             origin_name  has_args  cls_is_type     kind              type_when_params   th_1   th_2   th_3
'None':                                                  None                     NoneType                                    None     False        False  'builtin'                         False  False  False  False
'ByteString':                               typing.ByteString  typing._SpecialGenericAlias              collections.abc.ByteString     False        False   'typing'                         False  False  False  False
'Hashable':                                   typing.Hashable  typing._SpecialGenericAlias                collections.abc.Hashable     False        False   'typing'                         False  False  False  False
'Sized':                                         typing.Sized  typing._SpecialGenericAlias                   collections.abc.Sized     False        False   'typing'                         False  False  False  False
'str':                                                    str                         type                                    None     False         True  'builtin'                         False  False  False  False
'int':                                                    int                         type                                    None     False         True  'builtin'                         False  False  False  False
'float':                                                float                         type                                    None     False         True  'builtin'                         False  False  False  False
'complex':                                            complex                         type                                    None     False         True  'builtin'                         False  False  False  False
'range':                                                range                         type                                    None     False         True  'builtin'                         False  False  False  False
'bool':                                                  bool                         type                                    None     False         True  'builtin'                         False  False  False  False
'bytes':                                                bytes                         type                                    None     False         True  'builtin'                         False  False  False  False
'bytearray':                                        bytearray                         type                                    None     False         True  'builtin'                         False  False  False  False
'memoryview':                                      memoryview                         type                                    None     False         True  'builtin'                         False  False  False  False
'NoneType':                                          NoneType                         type                                    None     False         True    'types'                         False  False  False  False
'GenericAlias':                            types.GenericAlias                         type                                    None      True         True    'types'                         False  False  False  False
'MethodDescriptorType':                     method_descriptor                         type                                    None     False         True    'types'                         False  False  False  False
'MethodWrapperType':                           method-wrapper                         type                                    None     False         True    'types'                         False  False  False  False
'WrapperDescriptorType':                   wrapper_descriptor                         type                                    None     False         True    'types'                         False  False  False  False
'BuiltinFunctionType':             builtin_function_or_method                         type                                    None     False         True    'types'                         False  False  False  False
'BuiltinMethodType':               builtin_function_or_method                         type                                    None     False         True    'types'                         False  False  False  False
'CellType':                                              cell                         type                                    None     False         True    'types'                         False  False  False  False
'ClassMethodDescriptorType':           classmethod_descriptor                         type                                    None     False         True    'types'                         False  False  False  False
'CodeType':                                              code                         type                                    None     False         True    'types'                         False  False  False  False
'CoroutineType':                                    coroutine                         type                                    None     False         True    'types'                         False  False  False  False
'DynamicClassAttribute':          types.DynamicClassAttribute                         type                                    None     False         True    'types'                         False  False  False  False
'EllipsisType':                                      ellipsis                         type                                    None     False         True    'types'                         False  False  False  False
'FrameType':                                            frame                         type                                    None     False         True    'types'                         False  False  False  False
'FunctionType':                                      function                         type                                    None     False         True    'types'                         False  False  False  False
'GeneratorType':                                    generator                         type                                    None     False         True    'types'                         False  False  False  False
'GetSetDescriptorType':                     getset_descriptor                         type                                    None     False         True    'types'                         False  False  False  False
'LambdaType':                                        function                         type                                    None     False         True    'types'                         False  False  False  False
'MemberDescriptorType':                     member_descriptor                         type                                    None     False         True    'types'                         False  False  False  False
'MethodType':                                          method                         type                                    None     False         True    'types'                         False  False  False  False
'ModuleType':                                          module                         type                                    None     False         True    'types'                         False  False  False  False
'NotImplementedType':                      NotImplementedType                         type                                    None     False         True    'types'                         False  False  False  False
'SimpleNamespace':                      types.SimpleNamespace                         type                                    None     False         True    'types'                         False  False  False  False
'TracebackType':                                    traceback                         type                                    None     False         True    'types'                         False  False  False  False
'UnionType':                                  types.UnionType                         type                                    None      True         True    'types'                         False  False  False  False
'_GeneratorWrapper':                  types._GeneratorWrapper                         type                                    None     False         True    'types'                         False  False  False  False
'ABCMeta':                                        abc.ABCMeta                         type                                    None     False         True   'typing'                         False  False  False  False
'Any':                                             typing.Any              typing._AnyMeta                                    None     False         True   'typing'                         False  False  False  False
'BinaryIO':                                   typing.BinaryIO                         type                                    None     False         True   'typing'                         False  False  False  False
'ForwardRef':                               typing.ForwardRef                         type                                    None     False         True   'typing'                         False  False  False  False
'Generic':                                     typing.Generic                         type                          typing.Generic     False         True   'typing'                         False  False  False  False
'NamedTupleMeta':                       typing.NamedTupleMeta                         type                                    None     False         True   'typing'                         False  False  False  False
'NewType':                                     typing.NewType                         type                                    None     False         True   'typing'                         False  False  False  False
'ParamSpec':                                 typing.ParamSpec                         type                                    None     False         True   'typing'                         False  False  False  False
'ParamSpecArgs':                         typing.ParamSpecArgs                         type                                    None     False         True   'typing'                         False  False  False  False
'ParamSpecKwargs':                     typing.ParamSpecKwargs                         type                                    None     False         True   'typing'                         False  False  False  False
'Protocol':                                   typing.Protocol         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'SupportsBytes':                         typing.SupportsBytes         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'SupportsComplex':                     typing.SupportsComplex         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'SupportsFloat':                         typing.SupportsFloat         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'SupportsIndex':                         typing.SupportsIndex         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'SupportsInt':                             typing.SupportsInt         typing._ProtocolMeta                                    None     False         True   'typing'                         False  False  False  False
'Text':                                                   str                         type                                    None     False         True   'typing'                         False  False  False  False
'TextIO':                                       typing.TextIO                         type                                    None     False         True   'typing'                         False  False  False  False
'TypeVar':                                     typing.TypeVar                         type                                    None     False         True   'typing'                         False  False  False  False
'TypeVarTuple':                           typing.TypeVarTuple                         type                                    None     False         True   'typing'                         False  False  False  False
'_AnnotatedAlias':                     typing._AnnotatedAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_AnyMeta':                                   typing._AnyMeta                         type                                    None     False         True   'typing'                         False  False  False  False
'_BaseGenericAlias':                 typing._BaseGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_BoundVarianceMixin':             typing._BoundVarianceMixin                         type                                    None     False         True   'typing'                         False  False  False  False
'_CallableGenericAlias':         typing._CallableGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_CallableType':                         typing._CallableType                         type                                    None     False         True   'typing'                         False  False  False  False
'_ConcatenateGenericAlias':   typing._ConcatenateGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_DeprecatedType':                     typing._DeprecatedType                         type                                    None     False         True   'typing'                         False  False  False  False
'_Final':                                       typing._Final                         type                                    None     False         True   'typing'                         False  False  False  False
'_GenericAlias':                         typing._GenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_Immutable':                               typing._Immutable                         type                                    None     False         True   'typing'                         False  False  False  False
'_LiteralGenericAlias':           typing._LiteralGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_LiteralSpecialForm':             typing._LiteralSpecialForm                         type                                    None     False         True   'typing'                         False  False  False  False
'_NamedTuple':                              typing.NamedTuple        typing.NamedTupleMeta                                    None     False         True   'typing'                         False  False  False  False
'_NotIterable':                           typing._NotIterable                         type                                    None     False         True   'typing'                         False  False  False  False
'_PickleUsingNameMixin':         typing._PickleUsingNameMixin                         type                                    None     False         True   'typing'                         False  False  False  False
'_ProtocolMeta':                         typing._ProtocolMeta                         type                                    None     False         True   'typing'                         False  False  False  False
'_SpecialForm':                           typing._SpecialForm                         type                                    None     False         True   'typing'                         False  False  False  False
'_SpecialGenericAlias':           typing._SpecialGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_TupleType':                               typing._TupleType                         type                                    None     False         True   'typing'                         False  False  False  False
'_TypedDict':                                typing.TypedDict        typing._TypedDictMeta                                    None     False         True   'typing'                         False  False  False  False
'_TypedDictMeta':                       typing._TypedDictMeta                         type                                    None     False         True   'typing'                         False  False  False  False
'_TypingEllipsis':                     typing._TypingEllipsis                         type                                    None     False         True   'typing'                         False  False  False  False
'_UnionGenericAlias':               typing._UnionGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_UnpackGenericAlias':             typing._UnpackGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'_alias':                         typing._SpecialGenericAlias                         type                                    None     False         True   'typing'                         False  False  False  False
'Coroutine':                                 typing.Coroutine  typing._SpecialGenericAlias               collections.abc.Coroutine     False        False   'typing'          typing._GenericAlias  False  False   True
'Generator':                                 typing.Generator  typing._SpecialGenericAlias               collections.abc.Generator     False        False   'typing'          typing._GenericAlias  False  False   True
'Callable':                                   typing.Callable         typing._CallableType                collections.abc.Callable     False        False   'typing'  typing._CallableGenericAlias  False   True  False
'AsyncGenerator':                       typing.AsyncGenerator  typing._SpecialGenericAlias          collections.abc.AsyncGenerator     False        False   'typing'          typing._GenericAlias  False   True  False
'ChainMap':                                   typing.ChainMap  typing._SpecialGenericAlias                    collections.ChainMap     False        False   'typing'          typing._GenericAlias  False   True  False
'DefaultDict':                             typing.DefaultDict  typing._SpecialGenericAlias                 collections.defaultdict     False        False   'typing'          typing._GenericAlias  False   True  False
'Dict':                                           typing.Dict  typing._SpecialGenericAlias                                    dict     False        False   'typing'          typing._GenericAlias  False   True  False
'ItemsView':                                 typing.ItemsView  typing._SpecialGenericAlias               collections.abc.ItemsView     False        False   'typing'          typing._GenericAlias  False   True  False
'Mapping':                                     typing.Mapping  typing._SpecialGenericAlias                 collections.abc.Mapping     False        False   'typing'          typing._GenericAlias  False   True  False
'MutableMapping':                       typing.MutableMapping  typing._SpecialGenericAlias          collections.abc.MutableMapping     False        False   'typing'          typing._GenericAlias  False   True  False
'OrderedDict':                             typing.OrderedDict  typing._SpecialGenericAlias                 collections.OrderedDict     False        False   'typing'          typing._GenericAlias  False   True  False
'Annotated':                                 typing.Annotated                         type                                    None     False         True   'typing'        typing._AnnotatedAlias  False   True   True
'AbstractSet':                             typing.AbstractSet  typing._SpecialGenericAlias                     collections.abc.Set     False        False   'typing'          typing._GenericAlias   True  False  False
'AsyncContextManager':             typing.AsyncContextManager  typing._SpecialGenericAlias  contextlib.AbstractAsyncContextManager     False        False   'typing'          typing._GenericAlias   True  False  False
'AsyncIterable':                         typing.AsyncIterable  typing._SpecialGenericAlias           collections.abc.AsyncIterable     False        False   'typing'          typing._GenericAlias   True  False  False
'AsyncIterator':                         typing.AsyncIterator  typing._SpecialGenericAlias           collections.abc.AsyncIterator     False        False   'typing'          typing._GenericAlias   True  False  False
'Awaitable':                                 typing.Awaitable  typing._SpecialGenericAlias               collections.abc.Awaitable     False        False   'typing'          typing._GenericAlias   True  False  False
'Collection':                               typing.Collection  typing._SpecialGenericAlias              collections.abc.Collection     False        False   'typing'          typing._GenericAlias   True  False  False
'Container':                                 typing.Container  typing._SpecialGenericAlias               collections.abc.Container     False        False   'typing'          typing._GenericAlias   True  False  False
'ContextManager':                       typing.ContextManager  typing._SpecialGenericAlias       contextlib.AbstractContextManager     False        False   'typing'          typing._GenericAlias   True  False  False
'Counter':                                     typing.Counter  typing._SpecialGenericAlias                     collections.Counter     False        False   'typing'          typing._GenericAlias   True  False  False
'Deque':                                         typing.Deque  typing._SpecialGenericAlias                       collections.deque     False        False   'typing'          typing._GenericAlias   True  False  False
'FrozenSet':                                 typing.FrozenSet  typing._SpecialGenericAlias                               frozenset     False        False   'typing'          typing._GenericAlias   True  False  False
'Iterable':                                   typing.Iterable  typing._SpecialGenericAlias                collections.abc.Iterable     False        False   'typing'          typing._GenericAlias   True  False  False
'Iterator':                                   typing.Iterator  typing._SpecialGenericAlias                collections.abc.Iterator     False        False   'typing'          typing._GenericAlias   True  False  False
'KeysView':                                   typing.KeysView  typing._SpecialGenericAlias                collections.abc.KeysView     False        False   'typing'          typing._GenericAlias   True  False  False
'List':                                           typing.List  typing._SpecialGenericAlias                                    list     False        False   'typing'          typing._GenericAlias   True  False  False
'MappingView':                             typing.MappingView  typing._SpecialGenericAlias             collections.abc.MappingView     False        False   'typing'          typing._GenericAlias   True  False  False
'Match':                                         typing.Match  typing._SpecialGenericAlias                                re.Match     False        False   'typing'          typing._GenericAlias   True  False  False
'MutableSequence':                     typing.MutableSequence  typing._SpecialGenericAlias         collections.abc.MutableSequence     False        False   'typing'          typing._GenericAlias   True  False  False
'MutableSet':                               typing.MutableSet  typing._SpecialGenericAlias              collections.abc.MutableSet     False        False   'typing'          typing._GenericAlias   True  False  False
'Pattern':                                     typing.Pattern  typing._SpecialGenericAlias                              re.Pattern     False        False   'typing'          typing._GenericAlias   True  False  False
'Reversible':                               typing.Reversible  typing._SpecialGenericAlias              collections.abc.Reversible     False        False   'typing'          typing._GenericAlias   True  False  False
'Sequence':                                   typing.Sequence  typing._SpecialGenericAlias                collections.abc.Sequence     False        False   'typing'          typing._GenericAlias   True  False  False
'Set':                                             typing.Set  typing._SpecialGenericAlias                                     set     False        False   'typing'          typing._GenericAlias   True  False  False
'Type':                                           typing.Type  typing._SpecialGenericAlias                                    type     False        False   'typing'          typing._GenericAlias   True  False  False
'ValuesView':                               typing.ValuesView  typing._SpecialGenericAlias              collections.abc.ValuesView     False        False   'typing'          typing._GenericAlias   True  False  False
'IO':                                               typing.IO                         type                                    None     False         True   'typing'          typing._GenericAlias   True  False  False
'SupportsAbs':                             typing.SupportsAbs         typing._ProtocolMeta                                    None     False         True   'typing'          typing._GenericAlias   True  False  False
'SupportsRound':                         typing.SupportsRound         typing._ProtocolMeta                                    None     False         True   'typing'          typing._GenericAlias   True  False  False
'Tuple':                                         typing.Tuple            typing._TupleType                                   tuple     False        False   'typing'          typing._GenericAlias   True   True   True
'list':                                                  list                         type                                    None     False         True  'builtin'            types.GenericAlias   True   True   True
'tuple':                                                tuple                         type                                    None     False         True  'builtin'            types.GenericAlias   True   True   True
'dict':                                                  dict                         type                                    None     False         True  'builtin'            types.GenericAlias   True   True   True
'set':                                                    set                         type                                    None     False         True  'builtin'            types.GenericAlias   True   True   True
'frozenset':                                        frozenset                         type                                    None     False         True  'builtin'            types.GenericAlias   True   True   True
'AsyncGeneratorType':                         async_generator                         type                                    None     False         True    'types'            types.GenericAlias   True   True   True
'MappingProxyType':                              mappingproxy                         type                                    None     False         True    'types'            types.GenericAlias   True   True   True
'defaultdict':                        collections.defaultdict                         type                                    None     False         True   'typing'            types.GenericAlias   True   True   True

"""
