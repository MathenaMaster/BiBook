#!/usr/bin/env python3

import os
import copy
from weakref import ref
from cnorm.nodes import *
from cnorm import nodes
import mymangling as mangling
import mykook as kook

class AtModule:
    def __init__(self, here, mname, statement):
        self.here = ref(here)
        self.mname = mname
        self.statement = statement
        print("AtModule here:", here)
        print("AtModule name:", mname)
        print("AtModule statement:", statement)
        ctype = ComposedType(self.mname)
        #ctype._identifier = self.mname
        ctype._identifier = mangling.mangle_symbol(self.mname, ctype) 
        base = Decl(ctype._identifier, ctype)
        base.fields = statement
        self.base = base
        #base = nodes.ComposedType(self.mname)
        #base._identifier = self.mname
        #base._specifier = Specifiers.STRUCT

        #self.base_decl = RootBlockStmt(ExprStmt(self.statement.body))
        #self.base_decl.bod
        #print("BASE_DECL:", base)
        print("FOLLOWING STATEMENT:", self)
        #print("FINAL NODE:", self.final_node)
        #self.statement = self.base_decl
        #self.statement.types.add(self.struct_base)
        print("")
    
    def doTrans(self):
        declared = []
        print("AtModule doTrans()")
        #self.statement.body._specifier = Specifiers.STRUCT
        #self.here().body.append(self.base)
        for decl in self.base.fields.body: #self.statement.body:
            print("Decl analyzed:", decl)
            decl._name = mangling.mangle_function(self.mname, decl._ctype, (str(decl._ctype._identifier) if isinstance(decl._ctype, ComposedType) else str(decl._name)))
            print("Mangled decl:", decl._name)
            #decl._ctype._specifier = Specifiers.STRUCT
            copied_decl = copy.deepcopy(decl)
            print("Adding:", copied_decl, "in types:", self.here().types)
            print("Of that here:", self.here())
            print("Appending decl:", copied_decl)
            print("To body:", self.here().body)
            self.here().body.append(copied_decl)
            #self.struct_base.body.append(copied_decl)
            declared.append(copied_decl)
            print("Declared now values:", declared)
        print("Before AtModule doTrans exit, declared now values:", declared)
        print("Last ADD struct statement:", self.statement.__dict__)
        print("")
        return declared

    #def Bib_to_c(self, ast, strct : nodes.ComposedType):
        #declared = []
        #ast.append(Raw("struct " + strct._identifier + " {"))
        #for decl in self.base.body:
            #decl._name = mangling.mangle_function(self.mname, decl._ctype, decl._name)
            #print("Mangled decl:", decl._name)
            #decl._ctype._specifier = Specifiers.STRUCT
            #copied_decl = copy.deepcopy(decl)
            #print("Adding:", copied_decl, "in types:", self.here().types)
            #print("Of that here:", self.here())
            #print("Appending decl:", copied_decl)
            #print("To body:", self.here().body)
            #self.here().body.append(copied_decl)
            #declared.append(copied_decl)
            #print("Declared now values:", declared)
        #ast.append(Raw("};"))
        #print("Before bib AtModule doTrans exit, declared now values:", declared)
        #print("Last bib ADD struct statement:", self.base.body.__dict__)
        #print("")
        #return declared

class AtImport:
    def __init__(self, here, fname, idx):
        self.here = ref(here)
        self.fname = fname.strip('"')
        self.idx = idx
        print("AtImport init filename:", self.fname, ", idx:", self.idx)
        print("here ref now values:", self.here())
        print("AtImport __init__ body before insertion is:", self.here().body)
        file_name, file_extension = os.path.splitext(self.fname)
        print("FILE EXTENTION:", file_extension)
        print("FILE NAME:", file_name)
        self.file_out_name = file_name + ".h"
        self.imported_tree, self.kooked_c = kook.get_tree(file_name + file_extension)
        print("Imported_tree values:", self.imported_tree)
        print("C CODE GOT:")
        print(self.kooked_c)
        print("ast body (not imported) now values:")
        print(self.here().body)
        print("")

    def doTrans(self):
        print("AtImport doTrans.")
        print("before insertion, idx is:", self.idx, "and entry file name is:", self.fname)
        print("AtImport doTrans before insertion body is:", self.here().body)
        print("REPLACING AtImport beg instance to c raw include named:", self.file_out_name)
        print( "at idx:", self.idx)
        included_raw = Raw("#include \"" + self.file_out_name + "\"\n")
        print("to include raw is:", included_raw)
        self.here().body[self.idx] = included_raw
        print("after insertion, idx is:", self.idx, "and final file name is:", self.file_out_name)
        print("in:", included_raw)
        print("after insertion, body is:", self.here())
        print("WRITING in", self.file_out_name, "the imported_tree:", self.imported_tree)
        print("valuing in C")
        print(self.kooked_c)
        print("Final AtImport doTrans() imported_tree:")
        print(self.imported_tree)
        print("")
        return self.imported_tree

class AtImplementation:
    def __init__(self, here, mname, statement):
        self.here = ref(here)
        self.mname = mname
        self.statement = statement
        print("AtImplementation here:", here)
        print("AtImplementation name:", mname)
        print("AtImplementation statement:", statement)
        print("")


    def doTrans(self):
        print("AtImplementation doTrans with statement body:", self.statement.body)
        for decl in self.statement.body:
            print("Decl tested:", decl)
            #symbol_name = mangling.mangle_symbol(self.mname, decl)
            #symbol_name = mangling.mangle_function(self.mname, decl._ctype, decl._name)
            mod_test = "_" + str(len(self.mname)) + str(self.mname)
            type_test = "_" + str(len(decl._ctype._identifier)) + str(decl._ctype._identifier)
            if mod_test not in decl._name and type_test not in decl._name:
                symbol_name = mangling.mangle_function(self.mname, decl._ctype, decl._name)
                print("Symbol name found:", symbol_name)
                print("For decl:", decl)
                print("Symbol test in here:", self.here())
                print("Symbol test in types.keys():", self.here().types.keys())
                decl._name = symbol_name
                self.here().body.append(decl)
                print("Implementation decl function name append:", symbol_name)
                print("Total decl is:", decl)
            else:
                print("Function name already mangled")
                print("Mangled decl is:", decl)
                print("ast now is:", self.here())
        print("")

class AtTypedCall:
    def __init__(self, here, var_type, mod, variable):
        self.here = ref(here)
        self.var_type = var_type
        self.mod = mod
        self.variable = variable
        print("AtTypedCall __init__ entry; type:", var_type, "module:", mod, "and variable name:", variable)
        print("AtTypedCall __init__ retained; type:", self.var_type, "module:", self.mod, "and variable name:", self.variable)
        self.var_type[0]._name = mangling.mangle_variable(self.mod, self.var_type[0], self.variable)
        self.var_type[0]._storage = nodes.Storages.EXTERN
        self.defined = []
        print("ATTYPEDCALL HERE:", self.here())
        print("With Extern storage value:", self.var_type[0]._storage)
        print("AtTypedCall init named:", self.var_type[0]._name, ", var_type:", self.var_type[0], ", module:", self.mod, ", nonmangled variable name:", self.variable)
        print(self.var_type[0]._name, "added to previous body that values now:")
        #self.here().body[0]._name = self.var_type[0]._name
        self.here().body.append(self.var_type)
        print(self.here().body[-1])
        print("")

    def doTrans(self, defined):
        print("AtTypedCall doTrans")
        symbol_name = mangling.mangle_variable(self.mod, self.var_type[0], self.variable)
        print("Symbol name found:", symbol_name)
        if symbol_name in self.var_type[0]._name:
            symbol = self.here().types[symbol_name]
            print("Symbol found and is:", symbol)
            print("Before body appending, body is:", self.here().body)
            print("ATTYPEDCALL DOTRANS:", symbol_name, "is next symbol to be added to body:", self.here().body)
        print("")

#class AtTypedCast:
#    def __init__(self, here, var_type, mod):
#        self.here = ref(here)
#        self.var_type = var_type
#        self.mod = mod
#        self.var_type._name = mangling.mangle_cast(self.mod, self.var_type)
#        self.defined = []
#        print("ATTYPEDCAST HERE:", self.here())
#        print("AtTypedCast init: var_type:", self.var_type, ", module:", self.mod, "and final name:", self.var_type._name)
#        print("")

#    def doTrans(self, defined):
#        print("AtTypedCast doTrans with defined:", defined)
#        self.defined = defined
#        symbol_name = mangling.mangle_cast(self.mod, self.var_type)
#        if symbol_name in self.here().types.keys():
#            symbol = self.here().types[symbol_name]
#            self.here().body.append(symbol)
#            print("ATTYPEDCAST DOTRANS:", symbol_name, "symbol added to body:", self.here().body)
#        print("")

#class AtTypedCallFunction:
#    def __init__(self, here, var_type, mod, function_name):
#        self.here = ref(here)
#        self.var_type = var_type
#        self.mod = mod
#        self.function = function_name
#        print("Function called:", self.function, "of mod:", self.mod, "of type:", self.var_type)
#        self.mangled_function_name = mangling.mangle_function(self.mod, var_type, self.function) #, self.params)
#        print("Mangled_function_name:", self.mangled_function_name)
#        print("Function now values:", self.function, "of mod:", self.mod, "of type:", self.var_type)
#        self.var_type._name = self.mangled_function_name
#        self.defined = []
#        print("ATTYPEDCALLFUNCTION HERE:", self.here())
#        print("AtTypedCallFunction init: nonmangled function name:", self.function, ", module:", self.mod, ", mangled function name:", self.mangled_function_name)
#        print("Mangled rewrite:", self.mangled_function_name)
#        print("")

#    def doTrans(self, defined_vars):
#        print("AtTypedCallFunction doTrans")
#        print("Tested body:", self.here().body)
#        for decl in self.here().body:
#            print("Decl tested in body:", decl)
#            symbol_name = mangling.mangle_function(self.mod, self.var_type, self.function) #, self.params)
#            print("Symbol name found:", symbol_name)
#            print("Analyzing in types.keys():", self.here().types.keys())
#            if symbol_name in self.here().types.keys():
#                symbol = self.here().types[symbol_name]
#                print("Symbol found:", symbol)
#                print("Before assignation, decl body:", decl.body)
#                print("In symbol body:", symbol.body)
#                symbol.body = decl.body
#                print("Before ast appending, ast body is:", self.here().body)
#                self.here().body.append(symbol)
#                break
#        print("End of AtTypedCallFunction")
#        print("With mangled function:", self.mangled_function_name)
#        print("")
