import pandas as pd
import itertools
import numpy as np
import sympy as sp
import re
import sys
import os
import ultis.basic_math as bm
#import matplotlib.pyplot as plt
#import networkx as nx
from collections import defaultdict, deque

class Boolean_algebra:
    def __init__(self, data = None, flag: bool = None):
        if flag is None:
            flag = bool(data)
        self.flag = flag
        self.data = data
        self.background_relationship = None
        self.bool_func = None

    def __add__(self, other):
        return Boolean_algebra(self.flag or other.flag)
    
    def __mul__(self, other):
        return Boolean_algebra(self.flag and other.flag)
    
    def __neg__(self):
        return Boolean_algebra(not self.flag)
    
    def __eq__(self, other):
        return Boolean_algebra(self.flag == other.flag)

    def __str__(self):
        return 'True' if self.flag else 'False'

    
    def _has_zero_one(self, x):
        zero = Boolean_algebra(False)
        one = Boolean_algebra(True)
        return Boolean_algebra(x+zero==x and x*one==x)

    def _differ_by_one_bit(self, a, b):
        diff = 0
        pos = -1
        for i in range(len(a)):
            if a[i] != b[i]:
                diff+=1
                pos = i
        return diff == 1, pos 

    def _combine_terms(self, a, b):
        ok, pos = self._differ_by_one_bit(a, b)
        if ok:
            copy_a = list(a)
            copy_a[pos] = '-'
            return tuple(copy_a)
        return None
     
    def _match_term_cell(self, term, cell):
        val_index = {'x':0, 'y':1, 'z':2, 't':3}
        k = 0
        while k < len(term):
            if term[k] == '-':
                match = term[k+1]
                if cell[val_index[match]] == '1':
                    return False
                k+=2
            else:
                if cell[val_index[term[k]]] == '0':
                    return False
                k+=1
        return True

    def __lt__(self, other):
        if not self.data:
            return True
        return self.data < other.data

    def _minterm(self):
        bool_func = self.bool_func.split('v')
        variables = sorted(set(v for v in self.bool_func if v.isalpha() and v != 'v'))
        all_minterms = set()
        for term in bool_func:
            base_vector = [None]*len(variables)
            for i, val in enumerate(variables):
                if f'-{val}' in term:
                    base_vector[i] = 0
                elif val in term:
                    base_vector[i] = 1
            
            missing_indices = [i for i, v in enumerate(base_vector) if v is None]

            for combination in itertools.product([0, 1], repeat=len(missing_indices)):
                new_minterm = list(base_vector)
                for i, val in enumerate(combination):
                    new_minterm[missing_indices[i]] = val
                all_minterms.add(tuple(new_minterm))
        return all_minterms, variables
    
    def _check_bool_func(func):
        def wrapper(self, *args, **kwargs):
            if not self.bool_func:
                raise ValueError("Boolean function is empty")
            return func(self, *args, **kwargs)
        return wrapper
    
# Khu vực hàm private

    #Luật giao hoán
    def commutative(self, x, y):
        return Boolean_algebra(x+y == y+x and x*y == y*x)
    
    #Luật kết hợp
    def associative(self, x, y, z):
        return Boolean_algebra((x+y)+z == x+(y+z) and (x*y)*z == x*(y*z))
    
    #Luật phân phối
    def distributive(self, x, y, z):
        return Boolean_algebra(x*(y+z)==(x*y)+(x*z) and x+(y*z)==(x+y)*(x+z))
    
    #Luật hấp thu
    def absorption(self, x, y):
        return Boolean_algebra(x+x*y == x and x*(x+y) == x)
    
    #luật bù
    def complemented(self, x):
        neg_x = -x
        zero = Boolean_algebra(False)
        one = Boolean_algebra(True)
        return Boolean_algebra(x+neg_x == one and x*neg_x == zero)
    
    #Luật luỹ đẳng
    def idempotent(self, x):
        return Boolean_algebra(x+x == x and x*x == x)
    
    #Luật trung hoà
    def neutral(self, x):
        zero = Boolean_algebra(False)
        one = Boolean_algebra(True)  
        return Boolean_algebra(x+zero == zero and x*one == one)
    
    #Luật De Morgan
    def DeMorgan(self, x, y):
        left = -(x+y)
        right = -x * -y
        left2 = -(x*y)
        right2 = -x + -y
        return Boolean_algebra(left == right and left2 == right2)

    #luật phủ định kép     
    def double_negation(self, x):
        return Boolean_algebra(-(-x) == x)

    #Luật đồng nhất
    def identity(self, x, y):
        return Boolean_algebra((x == y) == ((x+ y == x) and (x*y == x)))
    
    def set_bool_algebra(self, list_data: list):
        """ demo:
        list_data: [1, 2]
        self.bool_algebra: [set(), {1}, {2}, {1, 2}]"""
        if not isinstance(list_data, list):
            raise ValueError("data must be list")
        self.bool_algebra = []
        for i in range(2**len(list_data)):
            for j in itertools.combinations(list_data, i):
                self.bool_algebra.append(Boolean_algebra(data=frozenset(j)))
        self.bool_algebra.sort()
        return self.bool_algebra
    
    def set_bool_func(self, data: str):
        """
        Example:
        data: x-yzvxyz
        return:
        self.bool_func: x-yzvxyz"""
        data = data.replace(' ', '')
        if not isinstance(data, str):
            raise ValueError("Data must be str")
        for value in data:
            if value.isalpha() and value not in ['x', 'y', 'z', 't', 'v']:
                raise ValueError(f"Value {value} don't support, only support (x, y, z, t)") 
            if value not in ['-'] and not value.isalpha():
                raise ValueError(f"Operator {value} don't support")
        self.bool_func = data

    def create_lattice_boolean(self, lattice: list):
        result = []
        for i in lattice:
            if not isinstance(i, (int, bool)):
                raise ValueError("data must be int or bool")
            else:
                result.append(Boolean_algebra(i))
        self.background_relationship = result

    def check_distributed_compensation(self):
        """Kiêm tra đại số Boolean có phải là đại số bù phân phối hay không"""
        #Kiểm tra phân phối
        for x in self.background_relationship:
            for y in self.background_relationship:
                for z in self.background_relationship:
                    if not self.distributive(x, y, z).data:
                        return Boolean_algebra(False)
                    
        #Kiểm tra phần tử 0 và 1
        for x in self.background_relationship:
            if not self._has_zero_one(x).data:
                return Boolean_algebra(False)
            
        #Kiểm tra phần bù
        for x in self.background_relationship:
            if not self.complemented(x).data:
                return Boolean_algebra(False)
            
        return Boolean_algebra(True)
    
    #Lấy danh sách nguyên tử
    def atom(self):
        result = []
        zero = Boolean_algebra(False)
        for x in self.bool_algebra:
            check = True
            if (x == zero).flag:
                check = False
                continue
            for y in self.bool_algebra[1:]:
                if zero < y < x:
                    check = False
                    break
            if check:
                result.append(x.data)
        return result
    
    #lấy tự tối thiểu
    @_check_bool_func
    def minterm(self):
        bool_func = self.bool_func.split('v')
        result  = {}
        if '-v' in self.bool_func:
            raise ValueError("Minterm is not defined for don't care function")
        for key in bool_func:
            zero_flag = False
            for data in key:
                if data == '-':
                    zero_flag = True
                elif zero_flag:
                    result.setdefault(key, []).append('0')
                    zero_flag = False
                else:
                    result.setdefault(key, []).append('1')
        return result
    #Lấy tự tối đại
    @_check_bool_func
    def maxterm(self):
        bool_func = self.bool_func.split('v')
        if '-v' in self.bool_func:
            raise ValueError("Maxterm is not defined for don't care function")
        result  = {}
        for key in bool_func:
            one_flag = False
            for data in key:
                if data == '-':
                    one_flag = True
                elif one_flag:
                    result.setdefault(key, []).append('1')
                    one_flag = False
                else:
                    result.setdefault(key, []).append('0')
        return result
    
    @_check_bool_func
    def abbreviated_SOP(self):
        """Rút gọn biểu thức Boolen"""
        bool_func = self.bool_func
        minterms, variables = self._minterm()
        minterms = sorted(minterms, key= lambda x: x.count(1))

        prime_implicants = set()
        current_minterms = list(minterms)   
        while current_minterms:
            #Sắp xếp minterms vào bảng
            table_SOP = {}
            for data in current_minterms:
                table_SOP.setdefault(data.count(1), []).append(data)
            #Kết hợp các minterms            
            new_groups = set()
            marks = set()
            keys = sorted(table_SOP.keys())
            for i in range(len(keys)-1):
                k1, k2 = keys[i], keys[i+1]
                for val1 in table_SOP[k1]:
                    for val2 in table_SOP[k2]:
                        is_combine = self._combine_terms(val1, val2)
                        if is_combine:
                            new_groups.add(is_combine)
                            marks.add(val1)
                            marks.add(val2)
            for i in current_minterms:
                if i not in marks:
                    prime_implicants.add(i)
            
            if not new_groups:
                break
            current_minterms = new_groups

        final_terms = []
        for p in prime_implicants:
            terms_part = []
            for b, val in zip(p, variables):
                if b == 0:
                    terms_part.append(f'-{val}')
                elif b == 1:
                    terms_part.append(val)
            final_terms.append(''.join(terms_part))

        return ' + '.join(final_terms)
    
    @_check_bool_func
    def Karnaugh_chart(self):
        if len(set(v for v in self.bool_func if v.isalpha() and v != 'v')) !=4:
            raise ValueError("Karnaugh map only support 4 variables (x, y, z, t)")
        K_chart = [
                    ['0000', '0001', '0011', '0010'],
                    ['0100', '0101', '0111', '0110'],
                    ['1100', '1101', '1111', '1110'],
                    ['1000', '1001', '1011', '1010']
                    ]
        result = [[False for _ in range(4)] for a in range(4)]
        sop = self.abbreviated_SOP().replace(' ', '').split('+')
        for i in range(4):
            for j in range(4):
                flag = False
                for c in sop:
                    if self._match_term_cell(c, K_chart[i][j]):
                        flag = True
                        break
                result[i][j] = flag
        return result
    

    # def Draw_K_map(self):
    #     fig, ax = plt.subplots(figsize=(5, 5))

    #     data = np.array(self.Karnaugh_chart(), dtype=int)
    #     ax.imshow(data, cmap='Greens')

    #     # Kẻ lưới
    #     ax.set_xticks(np.arange(-.5, 4, 1), minor=True)
    #     ax.set_yticks(np.arange(-.5, 4, 1), minor=True)
    #     ax.grid(which='minor', color='black', linewidth=2)
    #     ax.tick_params(which='both', bottom=False, left=False)

    #     # Nhãn cột (x, y)
    #     ax.set_xticks([0, 1, 2, 3])
    #     ax.set_xticklabels(
    #         [r'$\bar{y}$', r'$y$', r'$y$', r'$\bar{y}$'],
    #         fontsize=12
    #     )

    #     # Nhãn hàng (z, t)
    #     ax.set_yticks([0, 1, 2, 3])
    #     ax.set_yticklabels(
    #         [r'$z\bar{t}$', r'$zt$', r'$\bar{z}t$', r'$\bar{z}\bar{t}$'],
    #         fontsize=12
    #     )

    #     # Nhãn biến phía trên
    #     for i, label in enumerate([r'$x$', r'$x$', r'$\bar{x}$', r'$\bar{x}$']):
    #         ax.text(i, -0.9, label, ha='center', va='center', fontsize=14)

    #     plt.show()
