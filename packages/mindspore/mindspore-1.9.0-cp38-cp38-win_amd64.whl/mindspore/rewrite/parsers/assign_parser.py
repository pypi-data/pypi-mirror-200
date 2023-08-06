# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Parse ast.Assign in construct function to node of SymbolTree."""
from __future__ import absolute_import
from typing import Union
import ast
import astunparse

from mindspore import log as logger
from mindspore._extends.parse.namespace import CellNamespace
from mindspore.nn import Cell
from mindspore.ops import operations as P
from mindspore.ops import Primitive
from ..symbol_tree import SymbolTree
from ..node import Node, TreeNode
from ..parser import Parser
from ..parser_register import reg_parser
from ..api.scoped_value import ScopedValue, ValueType
from ..symbol_tree_builder import SymbolTreeBuilder
from ..ast_helpers import AstReplacer, AstModifier
from ..common.event import Event
from ..namespace import is_subtree


class AssignParser(Parser):
    """Parse ast.Assign in construct function to node of SymbolTree."""

    def __init__(self):
        """Constructor"""
        super(AssignParser, self).__init__()
        self._cell_namespce = CellNamespace('mindspore.nn')
        self._primitive_namespce = CellNamespace('mindspore.ops.operations')

    def target(self):
        """Parse target type."""
        return ast.Assign

    @staticmethod
    def _create_scopedvalue_from_tuple_ast(node: ast.Tuple) -> ScopedValue:
        """
        Create ScopedValue from a tuple ast node.

        Args:
            node (ast.Tuple): A tuple node.

        Returns:
            An instance of ScopedValue.

        Raises:
            RuntimeError: Only support ast.Constant as elts of ast.Tuple.
        """
        tuple_elts = node.elts
        tuple_values = []
        for tuple_elt in tuple_elts:
            if not isinstance(tuple_elt, (ast.Constant, ast.Name)):
                raise RuntimeError("Only support ast.Constant or ast.Name as elts of ast.Tuple.")
            if isinstance(tuple_elt, ast.Constant):
                tuple_values.append(tuple_elt.value)
            elif isinstance(tuple_elt, ast.Name):
                tuple_values.append(tuple_elt.id)
        return ScopedValue.create_variable_value(tuple(tuple_values))

    @staticmethod
    def _create_scopedvalue(node: ast.expr) -> ScopedValue:
        """
        Create ScopedValue from an ast node.

        Args:
            node (ast.expr): An ast node.

        Returns:
            An instance of ScopedValue.

        Raises:
            RuntimeError: Value of target of ast.Assign should be an ast.Name when target is an ast.Attribute.
            RuntimeError: Type of input node is unsupported.
        """
        if isinstance(node, ast.Name):
            return ScopedValue.create_naming_value(node.id)
        if isinstance(node, ast.Attribute):
            scope = node.value
            if not isinstance(scope, ast.Name):
                raise RuntimeError("value of target of ast.Assign should be a ast.Name when target is a ast.Attribute.")
            return ScopedValue.create_naming_value(node.attr, scope.id)
        if isinstance(node, ast.Tuple):
            return AssignParser._create_scopedvalue_from_tuple_ast(node)
        if isinstance(node, ast.Constant):
            return ScopedValue.create_variable_value(node.value)
        if isinstance(node, ast.Num):
            return ScopedValue.create_variable_value(node.n)
        if isinstance(node, (ast.Str, ast.Bytes)):
            return ScopedValue.create_variable_value(node.s)
        raise RuntimeError("Unsupported ast type to argument:", node)

    @staticmethod
    def _get_func_name(ast_node: ast.Call) -> str:
        """
        Get the func name from ast.Call.

        Args:
            ast_node (ast.Call): Input ast.Call node.

        Returns:
            Func name.

        Raises:
            RuntimeError: Func of input ast node is not ast.Name or ast.Attribute.
        """
        func = ast_node.func
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
        if isinstance(func, ast.Call):
            return AssignParser._get_func_name(func)
        raise RuntimeError("FuncValue is should be Name or a Attribute or a Call:", astunparse.unparse(func))

    @staticmethod
    def _get_func_scope(ast_node: ast.Call) -> str:
        """
        Get the func scope from ast.Call.

        Args:
            ast_node (ast.Call): Input ast.Call node.

        Returns:
            Func scope.

        Raises:
            RuntimeError: FuncValue is not an ast.Name when func is an ast.Attribute.
            RuntimeError: Func of input ast node is not ast.Name or ast.Attribute.
        """
        func = ast_node.func
        if isinstance(func, ast.Name):
            return ""
        if isinstance(func, ast.Attribute):
            value = func.value
            if not isinstance(value, ast.Name):
                raise RuntimeError("FuncValue is should be Name:", ast.dump(func))
            return value.id
        if isinstance(func, ast.Call):
            return AssignParser._get_func_scope(func)
        raise RuntimeError("FuncValue should be Name or a Attribute or a Call:", ast.dump(func))

    @staticmethod
    def _get_symbol_object(symbol_name, origin_net):
        """
        Get the func scope from ast.Call.

        Args:
            symbol_name (str): Func name.
            origin_net ([nn.Cell]): Network instance.

        Returns:
            Symbol Object.
        """
        var_dict = origin_net.__dict__
        for key, value in var_dict["_cells"].items():
            if key == symbol_name:
                return value

        for key, value in var_dict["_primitives"].items():
            if key == symbol_name:
                return value
        return None

    @staticmethod
    def _create_kwargs(keywords: [ast.keyword]) -> {str, ScopedValue}:
        """
        Transfer ast.Call keywords to a dict of ScopedValue when creating a symbol tree node.

        Args:
            keywords ([ast.keyword]): Keywords of ast.Call node.

        Returns:
            A dict of ScopedValue.
        """
        results = {}
        for keyword in keywords:
            results[keyword.arg] = AssignParser._create_scopedvalue(keyword.value)
        return results

    @staticmethod
    def _find_op_and_type(func_scope, func_name, stree: SymbolTree):
        """
        Get the func scope from ast.Call.

        Args:
            func_scope (str): Func scope.
            func_name (str): Func name.
            stree (SymbolTree): Belong SymbolTree.

        Returns:
            A type represents type of op and an instance represents operator instance.
        """

        if func_scope != "self":
            logger.warning("Not support parse operator which is instantiated at runtime now: %s; name: %s", func_scope,
                           func_name)
        var_dict = stree.get_origin_network().__dict__
        for key, value in var_dict["_cells"].items():
            if key == func_name:
                return type(value), value

        for key, value in var_dict["_primitives"].items():
            if key == func_name:
                return type(value), value
        return type(None), None

    @staticmethod
    def _get_targets(all_targets: ScopedValue) -> [Union[ScopedValue, str]]:
        """Get targets from tuple or single value."""
        targets: [Union[ScopedValue, str]] = []
        if all_targets.type == ValueType.TupleValue:
            for single_target in all_targets.value:
                if not isinstance(single_target, ScopedValue) and not isinstance(single_target.value, str):
                    raise RuntimeError("Only support str target in tuple.")
                targets.append(single_target)
        else:
            targets.append(all_targets)
        return targets

    @staticmethod
    def _update_field_in_init(func_scope, func_name, stree: SymbolTree, sub_tree: SymbolTree) -> bool:
        """
        When node is an invoking to sub-network, update value of ast.Assign of corresponding field in `__init__` method.

        Update from:

        .. code-block::

        self.field = getattr(self._handler, "field")

        to:

        .. code-block::

        self.field = SubNetwork(global_vars.get("field_args"))

        Args:
            func_scope (str): A string represents scope of function symbol.
            func_name (str): A string represents function symbol.
            stree (SymbolTree): The SymbolTree corresponding to main-network.
            sub_tree (SymbolTree): The SymbolTree corresponding to sub-network.

        Raises:
            NotImplementedError: If `func_scope` is not "self", it means corresponding op is inited in forward method.
            NotImplementedError: If targets of ast.Assign of corresponding field in `__init__` method.
        """

        changed = False
        if func_scope != "self":
            logger.warning("Not support parse operator which is instantiated at runtime now: %s; name: %s", func_scope,
                           func_name)
        init_func_ast = stree.get_init_func_ast()
        class_name = sub_tree.get_opt_cls_name()
        for body in init_func_ast.body:
            if not isinstance(body, ast.Assign):
                continue
            if len(body.targets) > 1:
                raise NotImplementedError("Not support multi-targets in assign now!")
            target = body.targets[0]
            if not isinstance(target, ast.Attribute) or not (target.value, ast.Name) or target.value.id != "self":
                continue
            if target.attr != func_name:
                continue
            changed = True
            global_vars_key = ''.join([func_name, "_args"])
            stree.add_global_vars(global_vars_key, sub_tree.get_global_vars())
            args_call = AstModifier.create_call(ScopedValue.create_naming_value("get", "global_vars"),
                                                [ScopedValue.create_variable_value(global_vars_key)])
            body.value = ast.Call(func=ast.Name(class_name, ast.Store()), args=[args_call], keywords=[])
            break
        return changed

    @staticmethod
    def _convert_ast_binop_to_node(ast_node: ast.BinOp, father_ast_node: ast.Assign) -> Node:
        """convert ast.BinOp to Node"""

        # only support ast.Add now
        op = P.Add()
        func_ast = ast.Attribute(value=ast.Name(id='F', ctx=ast.Load()), attr='add', ctx=ast.Load())
        func = ScopedValue.create_naming_value('add', 'F')

        father_ast_node.value = ast.Call(func=func_ast, args=[ast_node.left, ast_node.right], keywords=[])
        targets = AssignParser._get_targets(AssignParser._create_scopedvalue(father_ast_node.targets[0]))
        call_args = [AssignParser._create_scopedvalue(arg) for arg in father_ast_node.value.args]
        return Node.create_call_buildin_op(op, father_ast_node, targets, func, call_args, {})

    def _convert_ast_call_to_node(self, ast_node: ast.Call, father_ast_node: ast.Assign, stree: SymbolTree) -> Node:
        """
        Convert ast.Call to a symbol tree node.

        Args:
            ast_node (ast.Call): An ast.Call of assign node in construct.
            father_ast_node (ast.Assign): Assign node in construct.
            stree (SymbolTree): Symbol Tree under parsing.

        Returns:
            An instance of Node in Symbol Tree.

        Raises:
            RuntimeError: If operator instance invoked by assign is undefined.
        """
        targets = AssignParser._get_targets(AssignParser._create_scopedvalue(father_ast_node.targets[0]))
        func_name = AssignParser._get_func_name(ast_node)
        if func_name is None or func_name == "":
            raise RuntimeError("function name not exist")
        func_scope = AssignParser._get_func_scope(ast_node)
        func = ScopedValue.create_naming_value(func_name, func_scope)
        call_args = [AssignParser._create_scopedvalue(arg) for arg in ast_node.args]
        call_kwargs = AssignParser._create_kwargs(ast_node.keywords)

        _, op = AssignParser._find_op_and_type(func_scope, func_name, stree)
        if op is None:
            raise RuntimeError("Operator instance undefined: '", astunparse.unparse(ast_node.func), "' of '",
                               astunparse.unparse(ast_node), "'")
        if isinstance(op, Primitive):
            return Node.create_call_buildin_op(op, father_ast_node, targets, func, call_args, call_kwargs, func_name)
        if isinstance(op, Cell):
            is_sub_tree = is_subtree(type(op).__name__)
            if is_sub_tree:
                stb = SymbolTreeBuilder(op)
                new_stree = stb.build()
                changed = AssignParser._update_field_in_init(func_scope, func_name, stree, new_stree)
                if changed:
                    # class SubSubNet:
                    #     def __init__(self, global_vars):
                    #         self._handler = global_vars.get("handler")
                    #
                    # class SubNet:
                    #     def __init__(self, global_vars):
                    #         self._handler = global_vars.get("handler")
                    #         self._subsubnet = None
                    #         if xxx:
                    #             self._subsubnet = SubSubNet(xxx)
                    #
                    # Assuming there are two instance of SubNet A and B. "if xxx" in A is True, and in B is False.
                    # So self._subsubnet in A is an instance of SubSubNet, and in B is None.
                    # So After rewrite, A's code:
                    # class SubNetA:
                    #     def __init__(self, global_vars):
                    #         self._handler = global_vars.get("handler")
                    #         self._subsubnet = SubSubNet(global_vars.get("subsubnet_args"))
                    # while B's code:
                    # class SubNetB:
                    #     def __init__(self, global_vars):
                    #         self._handler = global_vars.get("handler")
                    #         self._subsubnet = getattr(self._handler, "_subsubnet")
                    # So SubNet should use SubNetA as its code when _update_field_in_init return True.
                    # So SubNet should use SubNetB as its code when _update_field_in_init return False or undefined
                    # error will occur to "global_vars.get("subsubnet_args")".
                    stree.on_change(Event.CodeChangeEvent)
                # Sub-network in main-network is expressed as:
                # self._subnet = SubNet(global_vars.get("subnet_args"))
                # when subnet is changed, its class will change, take SubNet1 as new class-name, so code main-network
                # also need to change:
                # self._subnet = SubNet1(global_vars.get("subnet_args"))
                # so a change in sub-network should also be identified as a change in main-network.
                # so main-network should observe sub-network
                replacer = AstReplacer(new_stree.get_class_ast())
                replacer.replace_all(new_stree.get_ori_cls_name(), new_stree.get_opt_cls_name())
                return TreeNode.create_tree_node(new_stree, father_ast_node, targets, func, call_args, call_kwargs,
                                                 func_name, new_stree.get_origin_network())
            return Node.create_call_buildin_op(op, father_ast_node, targets, func, call_args, call_kwargs, func_name)
        raise RuntimeError("Only support Cell operator or Primitive operator, got ", type(op).__name__)

    def process(self, stree: SymbolTree, node: ast.Assign):
        """
        Parse ast.Assign and create a node in symbol tree.

        - Create node when value of ast.Assign is in [ast.Call, ast.Name, ast.Constant, ast.Attribute].
        - Create python node when value of ast.Assign is in [ast.BinOp, ast.BoolOp, ast.Subscript, ast.List, ast.Tuple,
          ast.Dict].
        - Other value types are not supported.

        Args:
            stree ([SymbolTree]): Symbol Tree under parsing.
            node ([ast.Assign]): An ast.Assign node.

        Raises:
            RuntimeError: Only support one target in assign now.
            RuntimeError: Unsupported node type in construct function.
        """

        targets = node.targets
        if len(targets) != 1:
            raise RuntimeError("Only support one target in assign now")
        value = node.value
        if isinstance(value, ast.Call):
            node_ = self._convert_ast_call_to_node(value, node, stree)
            stree.append_origin_field(node_)
        elif isinstance(value, ast.BinOp):
            if isinstance(value.op, ast.Add):
                node_ = AssignParser._convert_ast_binop_to_node(value, node)
                stree.append_origin_field(node_)
            else:
                logger.info(f"ops-call({astunparse.unparse(node)}) in assign will be supported in near feature, "
                            f"ignored as a python node now")
                stree.try_append_python_node(node, node)
        elif isinstance(value, (ast.BoolOp, ast.Subscript)):
            logger.info(f"ops-call({astunparse.unparse(node)}) in assign will be supported in near feature, "
                        f"ignored as a python node now")
            stree.try_append_python_node(node, node)
        elif isinstance(value, (ast.Name, ast.Constant, ast.Attribute, ast.Num, ast.NameConstant, ast.Bytes, ast.Str)):
            if isinstance(value, ast.Name):
                node_name = "name_assign"
            elif isinstance(value, ast.Constant):
                node_name = "constant_assign"
            else:
                node_name = "attribute_assign"
            targets = AssignParser._get_targets(AssignParser._create_scopedvalue(node.targets[0]))
            call_args = [AssignParser._create_scopedvalue(value)]
            node_ = Node.create_call_pass_through_method(node, targets, call_args, {}, node_name)
            stree.append_origin_field(node_)
        elif isinstance(value, ast.Tuple):
            targets = AssignParser._get_targets(AssignParser._create_scopedvalue(node.targets[0]))
            args = []
            for elt in value.elts:
                args.append(AssignParser._create_scopedvalue(elt))
            node_ = Node.create_call_method(node, targets, ScopedValue.create_naming_value("tuple"), args, {}, "tuple")
            stree.append_origin_field(node_)
        elif isinstance(value, (ast.List, ast.Dict)):
            # add these as callmethod node if necessary
            stree.try_append_python_node(node, node)
        else:
            raise RuntimeError(f"Unsupported statement({astunparse.unparse(node)}) in construct function!")


g_assign_parser = reg_parser(AssignParser())
