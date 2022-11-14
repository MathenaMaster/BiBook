#!/usr/bin/env python3

import copy
from weakref import ref
from pyrser import meta
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm.parsing.expression import Expression
from cnorm import nodes
from cnorm.nodes import *
from cnorm.passes import to_c

import mymodule as module

class KOOK(Declaration, Grammar):
    entry = "translation_unit"
    grammar = """

        kook_primary_expression =
        [
            Declaration.primary_expression:>_
            | kook_instruction #new_kook_id(_)
        ]

        expression_kook_primary_expression =
        [
            Expression.primary_expression:>_
            | kook_instruction #new_kook_id(_)
        ]

        get_kook_ident =
        [
            '(' type_name:type ')' id:mod '.' id:var #add_kook_ident(type, mod, var)
        ]

        kook_var =
        [
            get_kook_ident #add_typed_call_variable(current_block)
        ]

        kook_instruction =
        [
            [ '[' kook_var ']' ]
        ]

        primary_expression = [
            "({"
                __scope__:current_block
                #new_blockexpr(_, current_block)
                [
                    line_of_code
                ]*
            "})"
            | // TODO: create special node for that
                "__builtin_offsetof"
                '(' [type_name ',' postfix_expression]:bof ')'
                #new_builtoffset(_, bof)
            |
            expression_kook_primary_expression:>_
        ]

        conditional_expression =
        [
            Expression.conditional_expression:>_
            | kook_instruction #new_kook_id(_)
        ]

        postfix_expression = [
            expression_kook_primary_expression:>_
            [
                __scope__:pres
                [
                '[' expression:expr ']' #new_array_call(pres, _, expr)
                | '(' func_arg_list?:args ')' #new_func_call(pres, _, args)
                | '.' identifier:i #new_dot(pres, _, i)
                | "->" identifier:i #new_arrow(pres, _, i)
                | ["++"|"--"]:op #new_raw(op, op) #new_post(pres, op, _)
                ]
                #bind('_', pres)
            ]*
        ]

    
        declaration =
        [
            [ kook_import
            | kook_module
            | kook_implementation
            | kook_class
            | Declaration.declaration ]
        ]

        kook_import =
        [
            "import" string:to_include
            #add_import(current_block, to_include)
        ]

        kook_module =
        [
            "module" id:id Statement.compound_statement:st
            #add_module(current_block, id, st)
        ]

        kook_implementation =
        [
            "implementation" id:id Statement.compound_statement:st
            #add_implementation(current_block, id, st)
        ]

        kook_class =
        [
            "class" id:id Statement.compound_statement:st
            #add_class(current_block, id, st)
        ]
        """

def __init__(self):
    self.id_mod = ""
    self.id_item = ""
    self.type_called = None
    self.id_func = ""

def transfo(ast, file, defined_vars : list):
    root = ast.body
    lenroot = len(root)
    defined_files = []
    print("TRANSFO BODY:", root)
    print("And len:", lenroot)
    for it in range(0, lenroot):
        print("it:", it, "root[it] instance", root[it])
        print("OF:", root)
        for decl in root:
            print("TRANSFO DECL:", decl)
            if isinstance(decl, module.AtModule):
                print("AtModule doTrans with definition:", decl)
                defined_vars += decl.doTrans()
                print("definition result:", defined_vars)
            elif isinstance(decl, module.AtTypedCall):
                print("AtTypedCall doTrans")
                decl.doTrans(defined_vars)
            elif isinstance(decl, module.AtTypedCallFunction):
                print("AtTypedCallFunction doTrans")
                decl.doTrans(defined_vars)
            elif isinstance(decl, module.AtTypedCast):
                print("AtTypedCast doTrans")
                decl.doTrans(defined_vars)
            elif isinstance(decl, module.AtImplementation):
                print("AtImplementation doTrans")
                decl.doTrans()
            elif isinstance(decl, module.AtImport):
                print("AtImport doTrans")
                if decl.fname not in defined_files:
                    print("file:", decl.fname, "not in defined files.")
                    defined_files.append(decl.fname)
                else:
                    print("treated file:", decl.fname)
                    continue
                    #print("treated file:", decl.fname)
                #else:
                    #print("treated file:", decl.fname)
                print("treated file:", decl.fname)
                defined = decl.doTrans() #it, file)
                print("ADDED DEFINITION:", defined)
                defined_vars.append(defined)
                print("DEFINITIONS IMPORT defined_vars:", defined_vars)
            elif hasattr(decl, 'body'):
                for instance in decl:
                    print("TRANSFO instance:", instance)
                    if isinstance(instance, module.AtModule):
                        print("AtModule doTrans with definition:", instance)
                        defined_vars += instance.doTrans()
                        print(defined_vars)
                    elif isinstance(instance, module.AtTypedCall):
                        print("AtTypedCall doTrans")
                        instance.doTrans(defined_vars)
                    elif isinstance(instance, module.AtTypedCallFunction):
                        print("AtTypedCallFunction doTrans")
                        instance.doTrans(defined_vars)
                    elif isinstance(instance, module.AtTypedCast):
                        print("AtTypedCast doTrans")
                        instance.doTrans(defined_vars)
                    elif isinstance(instance, module.AtImplementation):
                        print("AtImplementation doTrans")
                        instance.doTrans()
                    elif isinstance(instance, module.AtImport):
                        print("AtImport doTrans")
                        if instance.fname not in defined_files:
                            print("file:", instance.fname, "not in defined files.")
                            defined_files.append(instance.fname)
                        else:
                            print("treated file body:", instance.fname)
                            continue
                        print("treated file:", instance.fname)
                        defined = instance.doTrans(it, file)
                        print("ADDED DEFINITION:", defined)
                        defined_vars.append(defined)
                        print("DEFINITIONS IMPORT defined_vars:", defined_vars)
    print("LEAVNG TRANSFO WITH DEFINED:", defined_vars)
    return defined_vars

def clean(ast):
    root = ast.body
    poplist = []
    it = 0
    for it in range(0, len(root)):
        if isinstance(root[it], module.AtImport):
            poplist.append(it)
        elif isinstance(root[it], module.AtModule):
            poplist.append(it)
        elif isinstance(root[it], module.AtImplementation):
            poplist.append(it)
        elif isinstance(root[it], module.AtTypedCall):
            poplist.append(it)
        elif isinstance(root[it], module.AtTypedCallFunction):
            poplist.append(it)
        elif isinstance(root[it], module.AtTypedCast):
            poplist.append(it)
        if hasattr(root[it], 'body'):
            clean(root[it])
    for i in reversed(poplist):
        root.pop(i)
    
def get_tree(file):
    defined_vars = []
    print("IN GET_TREE WITH FILE:", file)
    res = KOOK().parse_file(file)
    print("IN GET_TREE AFTER PARSE FILE:", res)
    if hasattr(res, 'Diagnostic') and res.diagnostic.have_errors:
        print("KOOK PARSE FAILED!")
        print(res.diagnostic.get_content())
        raise
    else:
        defined = transfo(res, file, defined_vars)
        print("RES DICT:")
        print(res.__dict__)
        clean(res)
        print("writing in file:", file, "C/H contents")
        as_name, as_ext = file.split('.')
        content = str(c_to_file(as_name, as_ext, res.body))
        print("c_to_file content writen:")
        print(content)
        return defined, content
    
def c_to_file(name, ext, content):
    print("Content of the future file:", name + "." +  ext, "values now:")
    broken_arm = ""
    for decl in content:
        print("working on:", decl)
        print("decl dict:", decl.__dict__)
        print("to_c getattr values:", getattr(decl, str('to_c')))
        print("callable is:", callable(getattr(decl, str('to_c'))))
        if hasattr(decl, "body"):
            print("Decl has BODY, not to_c:", decl)
            print("with body:", decl.body)
            broken_arm += str(decl.to_c())
        else:
            broken_arm += str(decl.to_c())
    translated_file = open(name + "." + ext.replace('k', ''), "w")
    if translated_file.writable():
        print("translated_file opened in:", translated_file.name)
        wrotelen = translated_file.write(str(broken_arm))
        if wrotelen > 0:
            print("Content of:", wrotelen, "bytes length to write in file:", translated_file.name) #name + "." + ext)
            print("C/H content wrote in file:", translated_file.name)
            print("C/H Content:")
            print(str(broken_arm))
        else:
            print("nothing has been writen")
    else:
        print("could not open c/h file.")
        raise
    return str(broken_arm)

def get_tree_to_c(file):
    res = KOOK().parse_file(file)
    if hasattr(res, 'Diagnostic') and res.diagnostic.have_errors:
        print(res.diagnostic.get_content())
    else:
        transfo(res, file)
        clean(res)
    content = res.to_c()
    return content

@meta.hook(KOOK)
def add_import(self, ast, ident : str):
    print("TROLL PRINT:", self.__dict__)
    print("Rule nodes:", self.rule_nodes)
    print("Tag_cache:", self.tag_cache)
    if hasattr(self, 'diagnostic') and self.diagnostic.have_errors:
        print("KOOK PARSE FAILED with:", self.diagnostic.__dict__)
        print(self.diagnostic.get_content())
        print(self.rule_nodes)
    print("AtImport ast node actually values:", ast)
    print("AtImport ast node __dict__ values:", ast.__dict__)
    beg = module.AtImport(ast.ref, self.value(ident), len(ast.ref.body))
    if hasattr(self, 'Diagnostic') and self.diagnostic.have_errors:
        print("KOOK PARSE FAILED with:", self.diagnostic.__dict__)
        print("diagnostic content:", self.diagnostic.get_content())
        print("Rule_nodes content:", self.rule_nodes)
    ast.ref.body.append(beg)
    print("beg dict:", beg.__dict__)
    print("AT_IMPORT IMPORTED_TREE:", beg.imported_tree)
    print("file:", beg.fname, "has been treated with idx:", beg.idx)
    return True

@meta.hook(KOOK)
def add_module(self, ast, mname, statement):
    beg = module.AtModule(ast.ref, self.value(mname), statement)
    ast.ref.body.append(beg)
    print("beg in ADD_MODULE:", beg, "beg dict:", beg.__dict__)
    return True
    
@meta.hook(KOOK)
def add_implementation(self, ast, mname, statement):
    beg = module.AtImplementation(ast.ref, self.value(mname), statement)
    self.id_func = self.value(mname)
    ast.ref.body.append(beg)
    print("Beg in add_impementation:", beg.__dict__)
    return True

@meta.hook(KOOK)
def add_assign(self, ast, mytype, owner, variable, othvar):
    beg = module.AtAssign(ast.ref, mytype, self.value(owner), self.value(variable), self.value(othvar))
    ast.ref.body.append(beg)
    print("dict:", beg.__dict__)
    return True


@meta.hook(KOOK)
def new_kook_id(self, ast):
    ast.set(nodes.Id(copy.deepcopy(self.type_called._name)))
    return True

@meta.hook(KOOK)
def add_typed_call_cast(self, ast, mod, var_type):
    beg = module.AtTypedCast(ast.ref, var_type, self.value(mod))
    ast.ref.body.append(beg)
    print("BEG IN ADD_TYPED_CAST_VARIABLE:", beg.__dict__)
    return True

meta.hook(KOOK)
def add_kook_element(self, current_block, kook_element):
    print("kook element caught:", kook_element.__dict__)
    print("in current_block:", current_block.__dict__)


@meta.hook(KOOK)
def add_typed_call_variable(self, ast):
    print("TYPE:", self.type_called)
    print("MODULE:", self.id_mod)
    print("MYVARIABLE:", self.id_item)
    beg = module.AtTypedCall(ast.ref, self.type_called, self.id_mod, self.id_item) #var_type, self.value(mod), self.value(variable))
    print("AST add_typed_call_variable dict:")
    print(ast.__dict__)
    print("To insert name:", beg.var_type._name)
    self.type_called = beg.var_type
    print("In ast dict:")
    print(ast.__dict__)
    print("body dict:")
    print(ast.ref.body)
    return True

@meta.hook(KOOK)
def add_full_typed_call_variable(self, ast, var_type, mod, name):
    print("MYVARIABLE:", self.value(name))
    print("MODULE:", self.value(mod))
    print("TYPE:", var_type)
    beg = module.AtTypedCall(ast.ref, var_type, self.value(mod), self.value(name))
    print("Before adding full typed beg in ast body:", ast.ref.body)
    print("BEG IN ADD_FULL_TYPED_CALL_VARIABLE:", beg.__dict__)
    decl = ast.ref.body[0]
    print("DECL FROM ast.ref.body:", decl)
    print("Full variable association of variable:", beg.var_type._name)
    print("OPERATION SEEMS OK")
    return True


@meta.hook(KOOK)
def add_typed_call_function_declaration(self, ast):
    print("MYFUNCTION:", self.id_item)
    print("MODULE:", self.id_mod)
    print("MYTYPE:", self.type_called)
    #beg = module.AtTypedCallFunctionDeclaration(ast.ref , self.type, self.value(mod), self.value(function_name)) #, params)
    beg = module.AtTypedCallFunction(ast.ref, self.type_called, self.id_mod, self.id_item)
    print("BEG IN ADD_TYPED_CALL_FUNCTION_DECLARATION:", beg.__dict__)
    return True

@meta.hook(KOOK)
def add_typed_call_function(self, ast):
    print("MYFUNCTION:", self.id_item)
    print("MODULE:", self.id_mod)
    print("of global type:", self.type_called)
    beg = module.AtTypedCallFunction(ast.ref, self.type_called, self.id_mod, self.id_item) #, params)
    ast.ref.body.append(beg)
    print("BEG IN ADD_TYPED_CALL_FUNCTION:", beg.__dict__)
    return True

@meta.hook(KOOK)
def add_kook_ident(self, var_type, mod, ident_to_get):
    self.type_called = var_type
    self.id_mod = self.value(mod)
    self.id_item = self.value(ident_to_get)
    print("now ident to formulate values:", self.id_mod, "of type:", self.type_called, ", and of name:", self.id_item)
    return True


@meta.hook(KOOK)
def print_AtTypedCall(self, typename):
    print("call_variable with typename:", typename)
    return True

