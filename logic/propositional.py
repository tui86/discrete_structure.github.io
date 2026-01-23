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

class Logic_basis:
    """v:hợp
    ^:giao
    ~:phủ định
    >: kéo
    =: bằng
    +: loại trừ
    <: kéo 2 chiều"""
    def _hop(self, a, b):
        if a=='T' or b=='T':
            return 'T'
        return 'F'
    def _giao(self, a, b):
        if a=='T' and b=='T':
            return 'T'
        return 'F'
    def _phu_dinh(self, a):
        if a=='T':
            return 'F'
        return 'T'
    def _keo(self, a, b):
        return self._hop(self._phu_dinh(a), b)
    def _loai_tru(self, a, b):
        if a==b:
            return 'F'
        return 'T'
    def _keo_2_chieu(self, a, b):
        if a==b:
            return 'T'
        return 'F'
    
    PRECEDENCE = {
        '~': 5,
        '^': 4,
        'v': 3,
        '+': 2,
        '>': 1,
        '<': 0
    }
    OPERATORS = set(PRECEDENCE.keys())
    def _to_postfix(self, variables: str):
        output = []
        stack = []
        for token in variables:
            if (token.isalpha() and token !='v') or token in ('0', '1'):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and self.PRECEDENCE[stack[-1]] >= self.PRECEDENCE[token]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append('(')
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()
            else:
                raise ValueError(f"Invalid character: {token}")
        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())
        return output
    
    def create_truth_table(self, variables: str):
        """Trả về bảng chân trị của biểu thức logic
        variables example: x^y"""
        variables = variables.replace(' ','')
        data = self._to_postfix(variables)

        #Tạo bảng chân trị
        count_val = 0
        val = []
        for i in data:
            if i.isalpha() and i != 'v' and i not in val:
                val.append(i)
                count_val+=1
        table = {i: [] for i in val}
        table['result'] = []
        for values in itertools.product(['T', 'F'], repeat=count_val):
            env = dict(zip(val, values))
            for v in val:
                table[v].append(env[v])
            stack = []
            for token in data:
                if token.isalpha() and token !='v':
                    stack.append(env[token])
                elif token == '0':
                    stack.append('F')
                elif token == '1':
                    stack.append('T')
                elif token == '~':
                    a = stack.pop()
                    stack.append(self._phu_dinh(a))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append({
                        'v': self._hop,
                        '^': self._giao,
                        '+': self._loai_tru,
                        '>': self._keo,
                        '<': self._keo_2_chieu
                    }[token](a, b))
            table['result'].append(stack.pop())
        
        return pd.DataFrame(table) 
    
    def constant_true_constant_false(self, variables: str):
        truth_table=self.create_truth_table(variables)
        val_end=truth_table.columns[-1]
        col_end=truth_table[val_end]
        if (col_end == 'T').all():
            return 'Hằng đúng'
        elif (col_end == 'F').all():
            return 'Hằng sai'
        else:
            return 'Hằng vừa đúng vừa sai'
    
    def check_variable(self, variables: str):
        if variables.count('=')!=1:
            raise ValueError("Biểu thức không hợp lệ")
        VT, VP = variables[:variables.index('=')], variables[variables.index('=')+1:]
        truth_table_VT=self.create_truth_table(VT)
        truth_table_VP=self.create_truth_table(VP)
        col_VT = truth_table_VT.iloc[:, -1]
        col_VP = truth_table_VP.iloc[:, -1]
        return col_VP.equals(col_VT)