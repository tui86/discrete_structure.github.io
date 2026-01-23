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

class Phuong_phap_dem:
    def __init__(self):
        self.func = ""
        self.mapping = ""
        self.variables = []
        self.check_injective_complete = None
        self.check_surjective_complete = None
        self.check_bijective_complete = None
    def set_function(self, func: str):
        if not isinstance(func, str):
            raise ValueError("The function must be a string.")
        if "=" not in func:
            raise ValueError("The function must contain '='.")
        self.func = func.strip()
        self._check_function_syntax()

    def _check_function_syntax(self):
        VT, VP = map(str.strip, self.func.split("=", 1))
        if not VT or not VP:
            raise ValueError("Each side of the equation must be non-empty.")
        tokens = re.findall(r'[a-zA-Z_]\w*', self.func)
        math_funcs = {'sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', 'abs', 'e'}
        variables = sorted(set(t for t in tokens if t not in math_funcs))
        if len(variables) != 2:
            raise ValueError("The function must contain exactly two distinct variables.")
        self.variables = variables

    def _check_mapping(self, mapping: str):
        if not isinstance(mapping, str) or "->" not in mapping:
            raise ValueError("Mapping must be in form 'N->R', 'Z->C', etc.")
        domain, codomain = mapping.split("->")
        domain, codomain = domain.strip(), codomain.strip()
        valid_sets = {"N", "Z", "R", "R+", "C"}
        if domain not in valid_sets or codomain not in valid_sets:
            raise ValueError("Mapping must use only N, Z, R, R+ or C.")
        return domain, codomain

    def _create_range(self, s):
        return {
            'N': np.arange(0, 50),
            'Z': np.arange(-50, 51),
            'R': np.linspace(-10, 10, 201),
            'R+': np.linspace(1e-6, 10, 101),
            'C': [complex(x, y) for x in np.linspace(-5, 5, 11) for y in np.linspace(-5, 5, 11)]
        }[s]

    def _convert_to_basic_data_type(self, val):
        try:
            v = complex(val)
            if v.imag == 0:
                return int(v.real) if v.real.is_integer() else float(v.real)
            return v
        except:
            return val
    def check_injective(self, mapping: str, print_log=False):
        domain, codomain = self._check_mapping(mapping)
        VT, VP = map(str.strip, self.func.split("="))
        x_sym, y_sym = map(sp.Symbol, self.variables)

        f_left = sp.sympify(VT)
        f_right = sp.sympify(VP)
        domain_values = self._create_range(domain)
        is_injective = True

        if f_right.has(sp.Abs) or f_right.has(sp.Piecewise):
            if print_log:
                print(f"Hàm {self.func} chứa Abs hoặc Piecewise, xét từng miền riêng.")
            self.check_surjective_complete = False
            return False

        for val in domain_values:
            y_val = f_left.subs(y_sym, val)
            expr = sp.sympify(f"{VP}-({y_val})")
            try:
                sols = sp.solve(expr, x_sym)
            except NotImplementedError:
                sols = sp.solveset(expr, x_sym, domain=sp.S.Reals)
                if isinstance(sols, sp.ConditionSet):
                    print(f"Không thể giải nghiệm tường minh cho {self.func}. Bỏ qua kiểm tra surjective.")
                    self.check_injective_complete = False
                    return False
            if len(sols) > 1:
                sols_converted = [self._convert_to_basic_data_type(s) for s in sols]
                count_sols = []
                if codomain == 'N':
                    for s in sols_converted:
                        if isinstance(s, int) and s>=0:
                            count_sols.append(s)
                elif codomain == 'Z':
                    for s in sols_converted:
                        if isinstance(s, int):
                            count_sols.append(s)
                elif codomain == 'R':
                    for s in sols_converted:
                        if isinstance(s, (float, int)):
                            count_sols.append(s)
                elif codomain == 'R+':
                    for s in sols_converted:
                        if isinstance(s, (float, int)) and s>=0:
                            count_sols.append(s)
                elif codomain == 'C':
                    for s in sols_converted:
                        if isinstance(s, (complex, float, int)):
                            count_sols.append(s)
                if len(count_sols) > 1:
                    is_injective = False
                    if print_log:
                        print(f"Giá trị y={y_val} có {len(sols)} nghiệm: {sols_converted}")
        self.check_injective_complete = is_injective
        return is_injective

    def check_surjective(self, mapping: str, print_log=False):
        domain, codomain = self._check_mapping(mapping)
        VT, VP = map(str.strip, self.func.split("="))
        y, x = map(sp.Symbol, self.variables)
        VT, VP = sp.sympify(VT), sp.sympify(VP)
        dependent_var = y if VT.has(y) else x
        independent_var = x if dependent_var == y else y

        # --- B1: Tìm biểu thức hàm f ---
        try:
            sol = sp.solve(VT - VP, dependent_var)
            if len(sol) != 1:
                sol = sp.solve(VT - VP, independent_var)
                dependent_var, independent_var = independent_var, dependent_var
                if len(sol) != 1:
                    raise ValueError(f"Cannot express as single-valued function. Found {len(sol)} solutions: {sol}")
            f_expr = sol[0]
        except Exception:
            try:
                solset = sp.solveset(VT - VP, dependent_var, domain=sp.S.Reals)
                if isinstance(solset, sp.ConditionSet) or not solset:
                    if print_log:
                        print(f"Không thể biểu diễn {self.func} như hàm duy nhất (Abs, floor, ...).")
                    self.check_surjective_complete = False
                    return False
                f_expr = list(solset)[0]
            except Exception:
                if print_log:
                    print(f"Không thể giải biểu thức: {self.func}")
                self.check_surjective_complete = False
                return False

        # --- B2: Nếu có Abs hoặc Piecewise ---
        if f_expr.has(sp.Abs) or f_expr.has(sp.Piecewise):
            if print_log:
                print(f"Hàm {self.func} chứa Abs hoặc Piecewise, xét từng miền riêng.")
            self.check_surjective_complete = False
            return False

        # --- B3: Kiểm tra toàn ánh ---
        codomain_values = self._create_range(codomain)
        is_surjective = True

        def _is_real_value(expr):
            from sympy.assumptions import Q, ask
            try:
                res = ask(Q.real(expr))
                if res is True:
                    return True
                if res is False:
                    return False
                return not any(sym for sym in expr.atoms(sp.I))
            except Exception:
                return False

        domain_check = {
            'N': lambda v: v.is_integer and v >= 0,
            'Z': lambda v: v.is_integer,
            'R': lambda v: _is_real_value(v),
            'C': lambda v: True,
        }[domain]

        for val in codomain_values:
            sols = sp.solve(sp.Eq(f_expr, val), independent_var)
            if not sols:
                if print_log:
                    print(f"Không có nghiệm ánh xạ vào {val}")
                is_surjective = False
                continue

            valid_sols = [s for s in sols if domain_check(s)]
            if not valid_sols:
                if print_log:
                    print(f"Không có nghiệm hợp lệ ánh xạ vào {val}")
                is_surjective = False

        self.check_surjective_complete = is_surjective
        return is_surjective

    def check_bijective(self, mapping: str, print_log=False):
        if self.check_injective_complete == True and self.check_surjective_complete == True:
            self.check_bijective_complete = True
            return True
        elif self.check_injective_complete == False or self.check_surjective_complete == False:
            self.check_bijective_complete = False
            return False
        is_injective = self.check_injective(mapping, print_log)
        if not is_injective:
            self.check_bijective_complete = False
            return False
        is_surjective = self.check_surjective(mapping, print_log)
        self.check_bijective_complete = is_surjective
        return is_surjective
    
    def reverse_mapping(self, mapping: str, print_log=False):
        if not self.check_bijective(mapping, 0):
            raise ValueError("Hàm không phải song ánh, không thể tìm nghịch đảo.")
        VT, VP = map(str.strip, self.func.split('='))
        x_sym, y_sym = map(sp.Symbol, self.variables)
        if 'y' in VT:
            f_expr = sp.sympify(VP)
        else:
            f_expr = sp.sympify(VT)
        try:
            inv_solutions = sp.solve(sp.Eq(y_sym, f_expr), x_sym)
        except Exception as e:
            raise ValueError(f"Lỗi khi tìm nghịch đảo: {e}")
        if not inv_solutions:
            raise ValueError("Không thể tìm thấy hàm nghịch đảo.")
        inv_func = inv_solutions[0].simplify()
        if print_log:
            print(f"Hàm f(x) = {f_expr}")
            print(f"Nghịch đảo f⁻¹(y) = {inv_func}")
        domain, _ = self._check_mapping(mapping)
        domain_values = self._create_range(domain)
        reverse_pairs = []
        for val in domain_values:
            fx_val = self._convert_to_basic_data_type(f_expr.subs(x_sym, val))
            inv_val = self._convert_to_basic_data_type(inv_func.subs(y_sym, fx_val))
            reverse_pairs.append((fx_val, inv_val))
        return inv_func, reverse_pairs