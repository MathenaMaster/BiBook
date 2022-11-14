#!/usr/bin/env python3

from cnorm.nodes import *

def mangle_identifier(type):
    mangled_identifier = "_" + str(len(type._identifier)) + type._identifier
    if hasattr(type, '_qualifier') and type._qualifier == 1:
        mangled_identifier += "k"
    if hasattr(type, '_sign') and type._sign == 2:
        mangled_identifier += "u"
    if hasattr(type, '_specifier') and type._specifier == 4:
        mangled_identifier += "l"
    elif hasattr(type, '_specifier') and type._specifier == 6:
        mangled_identifier += "s"
    tmp = type._decltype
    while hasattr(tmp, '_decltype'):
        if isinstance(tmp, QualType) and tmp._qualifier == 1:
            mangled_identifier += "k"
        elif isinstance(tmp, PointerType):
            mangled_identifier += "p"
        tmp = tmp._decltype
    return mangled_identifier   

def mangle_identifier_from_name(type):
    mangled_identifier: str = ""
    if "const" in type:
        mangled_identifier += "const"
    if "unsigned" in type:
        mangled_identifier += "unsigned"
    if "long" in type:
        mangled_identifier += "long"
    elif "int" in type:
        mangled_identifier += "int"
    elif "short" in type:
        mangled_identifier += "short"
    elif "char" in type:
        mangled_identifier += "char"
    elif "void" in type:
        mangled_identifier += "void"
    elif "float" in type:
        mangled_identifier += "float"
    elif "double" in type:
        mangled_identifier += "double"
    if "*" in type:
        mangled_identifier += "p"
    print("mangled _identifier_from_name", mangled_identifier)
    final_mangle = "_" + str(len(mangled_identifier)) + mangled_identifier
    print("Final mangle:", final_mangle)
    return final_mangle

def mangle_function_identifier_from_name(fulltype, type):
    mangled_identifier: str = ""
    if "const" in type:
        mangled_identifier += "const"
    if "unsigned" in type:
        mangled_identifier += "unsigned"
    if "long" in type:
        mangled_identifier += "long"
    elif "int" in type:
        mangled_identifier += "int"
    elif "short" in type:
        mangled_identifier += "short"
    elif "char" in type:
        mangled_identifier += "char"
    elif "void" in type:
        mangled_identifier += "void"
    elif "float" in type:
        mangled_identifier += "float"
    elif "double" in type:
        mangled_identifier += "double"
    if "*" in type or isinstance(fulltype._decltype, PointerType):
        mangled_identifier += "p"
    print("mangled _identifier_from_name:", mangled_identifier)
    final_mangle = "_" + str(len(mangled_identifier)) + mangled_identifier
    print("Final mangle:", final_mangle)
    return final_mangle


def mangle_symbol(module_name, decl):
    mangled_name = "_" + str(len(module_name)) + module_name
    type = decl._ctype
    if isinstance(type, PrimaryType):
        mangled_name += mangle_identifier(type)
        mangled_name += "_" + str(len(decl._name)) + decl._name
    elif isinstance(type, FuncType):
        mangled_name += mangle_identifier(type)
        mangled_name += "_" + str(len(decl._name)) + decl._name
    return mangled_name

def mangle_cast(module_name, identifier):
    mangled_name = "_" + str(len(module_name)) + module_name
    mangled_name += mangle_identifier_from_name(identifier._identifer)
    return mangled_name

def mangle_variable(module_name, identifier, variable):
    print("MANGLE_VARIABLE Content, identifier:", identifier)
    print("MANGLE_VARIABLE Content, variable:", variable)
    print("MANGLE_VARIABLE Content, module:", module_name)
    mangled_name = "_" + str(len(module_name)) + module_name
    print("mangle_variable:", mangled_name, ",", module_name, ",", identifier._ctype._identifier, ",", variable)
    mangeled_id = mangle_function_identifier_from_name(identifier._ctype, identifier._ctype._identifier)
    mangled_name += str(mangeled_id)
    print("mangle_variable:", mangled_name, ",", module_name, ",", mangeled_id, ",", variable)
    mangled_variable = "_" + str(len(variable)) + variable
    mangled_name += mangled_variable
    print("mangle_variable:", mangled_name, ",", module_name, ",", mangeled_id, ",", mangled_variable)
    return mangled_name

def mangle_function(module_name, var_type, function_name):
    print("MANGLE_FUNCTION Content, identifier:", var_type)
    print("MANGLE_FUNCTION Content, variable:", function_name)
    print("MANGLE_FUNCTION Content, module:", module_name)
    mangled_name = "_" + str(len(module_name)) + str(module_name)
    print("Mangled mod:", mangled_name)
    mangled_type = mangle_function_identifier_from_name(var_type, var_type._identifier)
    print("Mangled func type:", mangled_type)
    mangled_name += str(mangled_type)
    mangled_func = "_" + str(len(function_name)) + str(function_name)
    print("Mangled func name:", mangled_func)
    mangled_name += str(mangled_func)
    print("Total mangeld func name:", mangled_name)
    return str(mangled_name)
    
def contains_variable(symbol_name, module_name, variable):
    module_name_number = int(symbol_name[1])
    if symbol_name[2:module_name_number] != module_name:
        return False
    return True
