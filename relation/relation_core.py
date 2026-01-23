import pandas as pd
import itertools
import numpy as np
import sympy as sp
import re
import sys
import os
import ultis.basic_math as bm
#import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque

class Relationship:
    #Khởi tao class
    def __init__(self):
        self.background_relationship=[]
        self.relationship=None
        self.is_reflective_relationship=False
        self.is_symmetrical_relationship=False
        self.is_bridging_relationship=False
        self.is_antisymmetric_relationship=False
        self.is_order_relationship=False
        self.operator = None
        self.powerset = []
#--- Khu vực hàm private---
    def _create_background_data(self, relationship):
        if self.background_relationship:
            return
        for i, j in relationship:
            if i not in self.background_relationship:
                self.background_relationship.append(i)
            if j not in self.background_relationship:
                self.background_relationship.append(j)
        self.background_relationship.sort()

    def _check_validable_data(self, relationship):
        for check_data_type in relationship:
            if not isinstance(check_data_type, (tuple, frozenset)):
                raise ValueError("data in list must be tuple or frozenset")
            if len(check_data_type) > 2:
                raise ValueError("data in list must have 2 or lower elements")
    
    def _check_identity_operator(self):
        for x, y in self.relationship:
            if x!=y:
                return False
        return True
    
    def _check_mod_operator(self):
        n = int(self.operator.split()[1])
        for x, y in self.relationship:
            if (x-y)%n != 0:
                return False
        return True
    
    def _check_divides_operator(self):
        for x, y in self.relationship:
            if not (x%y == 0 or y%x == 0):
                return False
        return True
    
    def _check_less_equal_operator(self):
        for x, y in self.relationship:
            if not (x <= y or y <= x):
                return False
        return True

    def _check_less_operator(self):
        for x, y in self.relationship:
            if not (x < y or y < x):
                return False
        return True

    def _check_greater_equal_operator(self):
        for x, y in self.relationship:
            if not (x >= y or y >= x):
                return False
        return True

    def _check_greater_operator(self):
        for x, y in self.relationship:
            if not (x > y or y > x):
                return False
        return True 

    def _check_subset_operator(self):
        for i , j in self.relationship:
            if not (i.issubset(j) or j.issubset(i)):
                return False
        return True
    
    def _check_proper_subset_operator(self):
        for i , j in self.relationship:
            if not ((i.issubset(j) or j.issubset(i) ) and i != j):
                return False
        return True
    
    def _check_superset_operator(self):
        for i , j in self.relationship:
            if not (i.issuperset(j) or j.issuperset(i)):
                return False
        return True
    
    def _check_proper_superset_operator(self):
        for i , j in self.relationship:
            if not ((i.issuperset(j) or j.issuperset(i)) and i != j):
                return False
        return True
    
    def _elements_from_relation(self):
        nodes = set()
        for a, b in self.relationship:
            nodes.add(a)
            nodes.add(b)
        return nodes
    
    # def _draw_hasse_diagram_int(self):
    #     G = nx.DiGraph()

    #     # Lấy danh sách node
    #     direct_subset_relations = self.create_hasse_diagram()
    #     nodes = set()
    #     for u, v in direct_subset_relations:
    #         nodes.add(u)
    #         nodes.add(v)

    #     for node in nodes:
    #         G.add_node(node)

    #     # Thêm cạnh
    #     for u, v in direct_subset_relations:
    #         G.add_edge(u, v)

    #     # Tính level của từng node
    #     level = {node: 0 for node in nodes}  # mặc định level = 0

    #     changed = True
    #     while changed:
    #         changed = False
    #         for u, v in direct_subset_relations:
    #             # Nếu u < v → level[v] phải ≥ level[u] + 1
    #             if u < v:
    #                 if level[v] < level[u] + 1:
    #                     level[v] = level[u] + 1
    #                     changed = True
    #             elif u > v:
    #                 if level[u] < level[v] + 1:
    #                     level[u] = level[v] + 1
    #                     changed = True

    #     # Gom node theo level
    #     levels = defaultdict(list)
    #     for node, lv in level.items():
    #         levels[lv].append(node)

    #     # Tọa độ vẽ
    #     pos = {}
    #     for lv, nodes_at_level in levels.items():
    #         num = len(nodes_at_level)
    #         for i, node in enumerate(nodes_at_level):
    #             pos[node] = (i - (num - 1) / 2, -lv)

    #     # Vẽ
    #     plt.figure(figsize=(10, 8))
    #     nx.draw(
    #         G, pos, with_labels=True,
    #         node_size=2000, node_color='lightblue',
    #         font_size=10, arrowstyle='->',
    #         arrowsize=20, edge_color='gray'
    #     )
    #     plt.title("Hasse Diagram")
    #     plt.show()

    def _sup(self, subset):
        '''Tìm chặn trên của tập con'''
        upper_bounds = set()
        for element in self.background_relationship:
            if all((s, element) in self.relationship for s in subset):
                upper_bounds.add(element)
        return upper_bounds
    
    def _inf(self, subset):
        '''Tìm chặn dưới của tập con'''
        lower_bounds = set()
        for element in self.background_relationship:
            if all((element, s) in self.relationship for s in subset):
                lower_bounds.add(element)
        return lower_bounds

    def _lub(self, subset):
        ubs = self._sup(subset)
        lubs = [x for x in ubs if all((y, x) not in self.relationship for y in ubs if y != x)]
        return lubs[0] if len(lubs) == 1 else None
    
    def _glb(self, subset):
        lbs = self._inf(subset)
        glbs = [x for x in lbs if all((x, y) not in self.relationship for y in lbs if y != x)]
        return glbs[0] if len(glbs) == 1 else None
    


#---Khu vực hàm private---            
    def set_relationship(self, relationship: list):
        self._check_validable_data(relationship)
        self._create_background_data(relationship)
        self.relationship=set(relationship)
        self.is_reflective_relationship = False
        self.is_symmetrical_relationship = False
        self.is_bridging_relationship = False
        self.is_antisymmetric_relationship = False
        self.is_order_relationship = False
        self.powerset = []

    def create_operator_relationship(self, background_relationship: list, operator: str):
        """Tạo quan hệ dựa trên toán tử và tập nền
        ví dụ: background_relationship = [1,2,3,4]
        operator = '|'
        thì self.background_relationship = [1,2,3,4]
        và self.relationship = {(1,1),(1,2),(1,3),(1,4),(2,2),(2,4),(3,3),(4,4)}
        """
        self.background_relationship = background_relationship
        result = set()
        powerset=[]
        if operator == '=':
            for data in self.background_relationship:
                result.add((data, data))
        elif operator == '|':
            for data in self.background_relationship:
                for data2 in self.background_relationship:
                    if data2%data == 0:
                        result.add((data, data2))
        elif operator.startswith('mod '):
            n = int(operator.split()[1])
            for a in self.background_relationship:
                for b in self.background_relationship:
                    if (a-b)%n == 0:
                        result.add((a, b))
        elif operator == '<=':
            for a in self.background_relationship:
                for b in self.background_relationship:
                    if a <= b:
                        result.add((a, b))
        elif operator == '<':
            for a in self.background_relationship:
                for b in self.background_relationship:
                    if a < b:
                        result.add((a, b))
        elif operator == '>=':
            for a in self.background_relationship:
                for b in self.background_relationship:
                    if a >= b:
                        result.add((a, b))
        elif operator == '>':
            for a in self.background_relationship:
                for b in self.background_relationship:
                    if a > b:
                        result.add((a, b))
        elif operator == 'subset':
            n = len(self.background_relationship)
            for i in range(n + 1):
                for comb in itertools.combinations(self.background_relationship, i):
                    powerset.append(frozenset(comb))
            for A in powerset:
                for B in powerset:
                    if A.issubset(B):
                        result.add((frozenset(A), frozenset(B)))
        elif operator == 'proper subset':
            n = len(self.background_relationship)
            for i in range(n + 1):
                for comb in itertools.combinations(self.background_relationship, i):
                    powerset.append(frozenset(comb))
            for A in powerset:
                for B in powerset:
                    if A.issubset(B) and A != B:
                        result.add((frozenset(A), frozenset(B)))
        elif operator == 'superset':
            n = len(self.background_relationship)
            for i in range(n + 1):
                for comb in itertools.combinations(self.background_relationship, i):
                    powerset.append(frozenset(comb))
            for A in powerset:
                for B in powerset:
                    if A.issuperset(B):
                        result.add((frozenset(A), frozenset(B)))
        elif operator == 'proper superset':
            n = len(self.background_relationship)
            for i in range(n + 1):
                for comb in itertools.combinations(self.background_relationship, i):
                    powerset.append(frozenset(comb))
            for A in powerset:
                for B in powerset:
                    if A.issuperset(B) and A != B:
                        result.add((frozenset(A), frozenset(B)))
        else:
            raise ValueError("Unsupported operator")
        self.set_relationship(result)
        self.operator = operator
        self.powerset = powerset
        return result

    def set_operator(self, operator: str):
        if operator not in ['=', '|', '<=', '<', '>=', '>', 'subset', 'proper subset', 'superset', 'proper superset'] and not operator.startswith('mod '):
            raise ValueError("Unsupported operator")
        self.operator = operator

    class Modulo:
        def modulo_congruence(self, var_a: int, var_b: int, print_log = False):
            if not isinstance(var_a, int) or not isinstance(var_b, int):
                raise ValueError("Var_a and var_b must be integer")
            n=bm.divisor(abs(var_a-var_b), print_log)
            return [i for i in n if i>1]
        
        def plus_modulo(self, var_a: int, var_c:int, var_b:int, var_d:int, print_log=False):
            VT=set(self.modulo_congruence(var_a, var_b, print_log=False))
            VP=set(self.modulo_congruence(var_c, var_d, print_log=False))
            result = sorted(VT & VP)
            if result and print_log:
                print(f"{var_a} + {var_c} đồng dư với {var_b} + {var_d}")
                print(f"Kết quả là: {result}")
            elif print_log:
                print(f"{var_a} + {var_c} không đồng dư với {var_b} + {var_d}")
            return result
        def minus_modulo(self, var_a: int, var_c:int, var_b:int, var_d:int, print_log=False):
            VT=set(self.modulo_congruence(var_a, var_b, print_log=False))
            VP=set(self.modulo_congruence(var_c, var_d, print_log=False))
            result = sorted(VT & VP)
            if result and print_log:
                print(f"{var_a} - {var_c} đồng dư với {var_b} - {var_d}")
                print(f"Kết quả là: {result}")
            elif print_log:
                print(f"{var_a} - {var_c} không đồng dư với {var_b} - {var_d}")
            return result
            
        def multiple_modulo(self, var_a:int, var_c:int, var_b:int, var_d:int, print_log=False):
            VT=set(self.modulo_congruence(var_a, var_b, print_log=False))
            VP=set(self.modulo_congruence(var_c, var_d, print_log=False))
            result = sorted(VT & VP)
            if result and print_log:
                    print(f"{var_a} * {var_c} đồng dư với {var_b} * {var_d}")
                    print(f"Kết quả là: {result}")
            elif print_log:
                    print(f"{var_a} * {var_c} không đồng dư với {var_b} * {var_d}")
            return result
        def exponential_modulo(self, var_a:int, var_b:int, m:int):
            base_mod = self.modulo_congruence(var_a, var_b)
            result = []
            for i in base_mod:
                if pow(var_a, m, i) == pow(var_b, m, i):
                    result.append(i)
            return result
        
    def check_reflective_relationship(self, prit_log=False):
        if not self.background_relationship:
            if prit_log:
                print("Tập nền rỗng")
            return False
        for data in self.background_relationship:
            if (data, data) not in self.relationship:
                if prit_log:
                    print("Không có quan hệ phản xạ")
                return False
        self.is_reflective_relationship = True
        return True
    
    def check_symmetrical_relationship(self, print_log=False):
        for x, y in self.relationship:
            if (y, x) not in self.relationship:
                if print_log:
                    print("không có quan hệ đối xứng")
                return False
        self.is_symmetrical_relationship = True
        return True
    
    def check_bridging_relationship(self, print_log=False):
        for x, y in self.relationship:
            for z in self.background_relationship:
                if (y, z) in self.relationship:
                    if (x, z) not in self.relationship:
                        if print_log:
                            print("không có quan hệ bắc cầu")
                        return False
        return True
    
    def check_equivalent_relationship(self, print_log=False):
        if self.is_reflective_relationship and self.is_symmetrical_relationship and self.is_bridging_relationship:
            return True
        elif self.check_reflective_relationship(print_log) and self.check_symmetrical_relationship(print_log) and self.check_bridging_relationship(print_log):
            return True
        return False
    
    def create_equivalence_class(self):
        # --- Tạo adjacency list ---
        adj = {x: set() for x in self.background_relationship}
        for a, b in self.relationship:
            adj[a].add(b)
            adj[b].add(a)  # quan hệ tương đương phải đối xứng

        visited = set()
        classes = []

        # --- DFS để gom nhóm ---
        def dfs(start, group):
            group.add(start)
            visited.add(start)
            for neighbor in adj[start]:
                if neighbor not in visited:
                    dfs(neighbor, group)

        # --- Tạo danh sách tất cả các lớp tương đương ---
        for x in self.background_relationship:
            if x not in visited:
                group = set()
                dfs(x, group)
                classes.append(sorted(group))

        # --- Chuyển sang dạng dictionary ---
        result = {}
        for group in classes:
            for element in group:
                result[element] = group

        return result
    
    def check_antisymmetric_relationship(self, print_log=False):
        for x, y in self.relationship:
            if (y, x) in self.relationship and x!=y:
                if print_log:
                    print("Không có quan hệ phản đối xứng")
                return False
        return True
    
    def check_order_relationship(self, print_log=False):
        if self.is_reflective_relationship and self.is_antisymmetric_relationship and self.is_bridging_relationship:
            self.is_order_relationship = True
            return True
        elif self.check_reflective_relationship(print_log) and self.check_antisymmetric_relationship(print_log) and self.check_bridging_relationship(print_log):
            self.is_order_relationship = True
            return True
        return False
    
    def check_total_order_relationship(self, print_log=False):
        if self.check_order_relationship(print_log):
            match self.operator:
                case '=':
                    return self._check_identity_operator()
                case '|':
                    return self._check_divides_operator()
                case op if op.startswith('mod '):
                    return self._check_mod_operator()
                case '<=':
                    return self._check_less_equal_operator()
                case '<':
                    return self._check_less_operator()
                case '>=':
                    return self._check_greater_equal_operator()
                case '>':
                    return self._check_greater_operator()
                case 'subset':
                    return self._check_subset_operator()
                case 'proper subset':
                    return self._check_proper_subset_operator()
                case 'superset':
                    return self._check_superset_operator()
                case 'proper superset':
                    return self._check_proper_superset_operator()
                case _:
                    raise ValueError("Unsupported operator")
        return False
    
    def maximal_elements(self):
        """Trả về các phần tử cực đại trong quan hệ thứ tự"""
        if not (self.is_order_relationship or self.check_order_relationship()):
            raise ValueError("Quan hệ không phải quan hệ thứ tự")
        maximal_elements = []
        for x in self.background_relationship:
            is_maximal = True
            for y in self.background_relationship:
                if (x, y) in self.relationship and x != y:
                    is_maximal = False
                    break
            if is_maximal:
                maximal_elements.append(x)
        return maximal_elements

    def covers(self, element):
        """Trả về các phần tử được bao phủ bởi phần tử đã cho trong quan hệ thứ tự"""
        if not (self.is_order_relationship or self.check_order_relationship()):
            raise ValueError("Quan hệ không phải quan hệ thứ tự")
        covers = []
        for y in self.background_relationship:
            if (element, y) in self.relationship and element != y:
                is_cover = True
                for z in self.background_relationship:
                    if (element, z) in self.relationship and (z, y) in self.relationship and element != z and z != y:
                        is_cover = False
                        break
                if is_cover:
                    covers.append(y)
        return covers

    def create_hasse_diagram(self):
        hasse_relationship = []
        if not self.powerset:
            sorted_powerset = sorted(self.background_relationship)
        else:
            sorted_powerset = sorted(self.powerset, key=len)
        for i in range(len(sorted_powerset)):
            for j in range(len(sorted_powerset)):
                a = sorted_powerset[i]
                b = sorted_powerset[j]
                if (a, b) in self.relationship and a != b:
                    is_cover = True
                    for k in range(len(sorted_powerset)):
                        if k != i and k != j:
                            c = sorted_powerset[k]
                            if (a, c) in self.relationship and (c, b) in self.relationship:
                                is_cover = False
                                break
                    if is_cover:
                        hasse_relationship.append((a, b))
        return hasse_relationship