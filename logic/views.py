from django.shortcuts import render
from .propositional import Logic_basis
from .boolean_algebra import Boolean_algebra
from .models import LogicModel
from functools import wraps
import ast

def count_logic_data(name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                counter, _ = LogicModel.objects.get_or_create(name=name)
                counter.count += 1
                counter.save()
            except Exception:
                pass  # không cho thống kê làm chết web
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


# Create your views here.
class PropositionalViews:
    
    def create_truth_table_views(request):
        return render(request, 'logic/truth_table.html')
    
    @count_logic_data('create_truth_table')
    def create_truth_table_compute(request):
        expression = request.GET.get('expression', '')
        logic = Logic_basis()
        try:
            truth_table = logic.create_truth_table(expression)
            truth_table = truth_table.to_html(classes='table table-sm', index=False, border=1, escape=False)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tạo bảng chân trị: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/truth_table.html', context)
        context = {
            'table': truth_table,
            'expression': expression,
        }
        return render(request, 'logic/truth_table.html', context)

    def constant_true_constant_false_views(request):
        return render(request, 'logic/constant_true_constant_false.html')
    
    @count_logic_data('constant_true_constant_false')
    def constant_true_constant_false_compute(request):
        expression = request.GET.get('expression', '')
        logic = Logic_basis()
        try:
            result = logic.constant_true_constant_false(expression)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/constant_true_constant_false.html', context)
        context = {
            'result': result,
            'expression': expression,
        }
        return render(request, 'logic/constant_true_constant_false.html', context)
    
    def check_variable_views(request):
        return render(request, 'logic/check_variable.html')
    
    @count_logic_data('check_variable')
    def check_variable_compute(request):
        expression = request.GET.get('expression', '')
        logic = Logic_basis()
        try:
            result=logic.check_variable(expression)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/check_variable.html', context)
        context = {
            'result': result,
            'expression': expression,
        }
        return render(request, 'logic/check_variable.html', context)
    
class Boolean_algebraViews:
    
    def caculator_boolean_algebra_views(request):
        return render(request, 'logic/caculator_boolean_algebra.html')
    
    @count_logic_data('caculator_boolean_algebra')
    def caculator_boolean_algebra_compute(request):
        expression = request.GET.get('expression', '')

        def eval_expr(expr, zero, one):
            node = ast.parse(expr, mode='eval')

            def _eval(n):
                # Binary operations
                if isinstance(n, ast.BinOp):
                    left = _eval(n.left)
                    right = _eval(n.right)

                    if isinstance(n.op, ast.Add):
                        return left + right
                    if isinstance(n.op, ast.Mult):
                        return left * right

                # Unary minus
                if isinstance(n, ast.UnaryOp):
                    if isinstance(n.op, ast.USub):
                        return -_eval(n.operand)

                # Constant: 0 or 1
                if isinstance(n, ast.Constant):
                    if n.value == 0:
                        return zero
                    if n.value == 1:
                        return one
                    raise ValueError("Only 0 and 1 are allowed")

                raise ValueError(f"Unsupported expression: {ast.dump(n)}")

            return _eval(node.body)
        
        one = Boolean_algebra(True, True)
        zero = Boolean_algebra(False, False)
        try:
            result = eval_expr(expression, zero, one)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/caculator_boolean_algebra.html', context)
        context = {
            'result': result,
            'expression': expression,
        }
        print(result)
        return render(request, 'logic/caculator_boolean_algebra.html', context)

    def check_boolean_algebra_properties_views(request):
        return render(request, 'logic/check_boolean_algebra_properties.html')
    
    @count_logic_data('check_boolean_algebra_properties')
    def check_boolean_algebra_properties_compute(request):
        property = request.GET.get('property', '')
        x_value = request.GET.get('x', '')
        y_value = request.GET.get('y', '')
        z_value = request.GET.get('z', '')
        convert = {'0': False, '1': True}
        try:
            x = Boolean_algebra(convert[x_value], convert[x_value])
            y = Boolean_algebra(convert[y_value], convert[y_value]) if y_value else None
            z = Boolean_algebra(convert[z_value], convert[z_value]) if z_value else None
            match property:
                case 'commutative':
                    result = x.commutative(x, y)
                case 'associative':
                    result = x.associative(x, y, z)
                case 'distributive':
                    result = x.distributive(x, y, z)
                case 'identity':
                    result = x.identity(x, y)
                case 'complement':
                    result = x.complemented(x)
                case 'idempotent':
                    result = x.idempotent(x)
                case 'absorption':
                    result = x.absorption(x, y)
                case 'de_morgan':
                    result = x.DeMorgan(x, y)
                case "double_negation":
                    result = x.double_negation(x)
                case 'neutral':
                    result = x.neutral(x)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'property': property,
                'x': x_value,
                'y': y_value,
                'z': z_value,
            }
            return render(request, 'logic/check_boolean_algebra_properties.html', context)
        context = {
            'result': result,
            'property': property,
            'x': x_value,
            'y': y_value,
            'z': z_value,
        }
        return render(request, 'logic/check_boolean_algebra_properties.html', context)
    
    def check_distributed_compensation_views(request):
        return render(request, 'logic/check_distributed_compensation.html')
    
    @count_logic_data('check_distributed_compensation')
    def check_distributed_compensation_compute(request):
        expression = request.GET.get('expression', '')
        logic = Boolean_algebra()
        convert = {'0': False, '1': True, 'False': False, 'True': True}
        try:
            lattice = []
            for val in expression.split(' '):
                if val in convert.keys():
                    lattice.append(convert[val])
                else:
                    raise ValueError(f"Giá trị không hợp lệ trong biểu thức: {val}")
            logic.create_lattice_boolean(lattice)
            result = logic.check_distributed_compensation()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/check_distributed_compensation.html', context)
        context = {
            'result': result,
            'expression': expression,
        }
        return render(request, 'logic/check_distributed_compensation.html', context)
    
    def atom_views(request):
        return render(request, 'logic/atom.html')
    
    @count_logic_data('atom')
    def atom_compute(request):
        expression = request.GET.get('expression', '')
        logic = Boolean_algebra()
        try:
            list_data = list(set(expression.split(' ')))
            logic.set_bool_algebra(list_data)
            result = logic.atom()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/atom.html', context)
        context = {
            'result': result,
            'expression': expression,
        }
        return render(request, 'logic/atom.html', context)
    
    def minterm_views(request):
        return render(request, 'logic/minterm.html')
    
    @count_logic_data('minterm')
    def minterm_compute(request):
        expression = request.GET.get('expression', '')
        logic = Boolean_algebra()
        try:
            logic.set_bool_func(expression)
            result = logic.minterm()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/minterm.html', context)
        context={
            'result': result,
            'expression': expression
        }
        return render(request, 'logic/minterm.html', context)
    
    def maxterm_views(request):
        return render(request, 'logic/maxterm.html')
    
    @count_logic_data('maxterm')
    def maxterm_compute(request):
        expression = request.GET.get('expression', '')
        logic = Boolean_algebra()
        try:
            logic.set_bool_func(expression)
            result = logic.maxterm()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/maxterm.html', context)
        context={
            'result': result,
            'expression': expression
        }
        return render(request, 'logic/maxterm.html', context)
    
    def abbreviated_SOP_views(request):
        return render(request, 'logic/abbreviated_SOP.html')
    
    @count_logic_data('abbreviated_SOP')
    def abbreviated_SOP_compute(request):
        expression = request.GET.get('expression', '')
        logic = Boolean_algebra()
        try:
            logic.set_bool_func(expression)
            result = logic.abbreviated_SOP()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính toán: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/abbreviated_SOP.html', context)
        context={
            'result': result,
            'expression': expression
        }
        return render(request, 'logic/abbreviated_SOP.html', context)
    
    def draw_Karnaugh_chart_views(request):
        return render(request, 'logic/draw_Karnaugh_chart.html')
    
    @count_logic_data('draw_Karnaugh_chart')
    def draw_Karnaugh_chart_compute(request):
        expression = request.GET.get('expression', ' ')
        logic = Boolean_algebra()
        try:
            logic.set_bool_func(expression)
            chart = logic.Karnaugh_chart()
            kmap = [[int(cell) for cell in row] for row in chart]
        except Exception as e:
            context = {
                'error': f"Lỗi khi tạo bản Karnaugh: {str(e)}",
                'expression': expression,
            }
            return render(request, 'logic/draw_Karnaugh_chart.html', context)
        
        GRAY = ['00', '01', '11', '10']

        rows = list(zip(GRAY, kmap))

        context = {
            'rows': rows,
            'col_labels': GRAY,
        }

        return render(request, 'logic/draw_Karnaugh_chart.html', context)