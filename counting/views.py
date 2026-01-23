from django.shortcuts import render
from .mapping import Phuong_phap_dem
from .pigeonhole import PigeonholePrinciple
from .models import CountingModel
from functools import wraps
import ast

def count_data(name):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            counter, _ = CountingModel.objects.get_or_create(name=name)
            counter.count += 1
            counter.save()
            return func(request)
        return wrapper
    return decorator

class CountingView:

    def check_injective_views(request):
        return render(request, 'counting/check_injective.html')

    @count_data('check_injective')
    def check_injective_compute(request):
        # read values safely with defaults and convert to strings
        domain = str(request.GET.get('domain', '')).strip()
        codomain = str(request.GET.get('codomain', '')).strip()
        mapping = f"{domain}->{codomain}"
        formula = request.GET.get('formula', '')

        # validate formula before calling mapping logic
        if not formula or '=' not in formula:
            context = {
                'error': "Vui lòng nhập ánh xạ theo dạng 'y=x' (phải chứa '=')",
                'formula': formula,
            }
            return render(request, 'counting/check_injective.html', context)

        result = Phuong_phap_dem()
        result.set_function(str(formula))
        try:
            is_injective = result.check_injective(mapping)
        except Exception as e:
            context = {
                'error': f"Lỗi khi kiểm tra đơn ánh: {str(e)}",
                'formula': formula,
            }
            return render(request, 'counting/check_injective.html', context)
        context={'result': is_injective}
        return render(request=request, template_name='counting/check_injective.html', context=context)

    def check_surjective_views(request):
        return render(request, 'counting/check_surjective.html')
    
    @count_data('check_surjective')
    def check_surjective_compute(request):
        domain = str(request.GET.get('domain', '')).strip()
        codomain = str(request.GET.get('codomain', '')).strip()
        mapping = f"{domain}->{codomain}"
        formula = request.GET.get('formula', '')
        if not formula or '=' not in formula:
            context = {
                'error': "Vui lòng nhập ánh xạ theo dạng 'y=x' (phải chứa '=')",
                'formula': formula,
            }
            return render(request, 'counting/check_surjective.html', context)
        result = Phuong_phap_dem()
        result.set_function(str(formula))
        try:
            is_surjective = result.check_surjective(mapping)
        except Exception as e:
            context = {
                'error': f"Lỗi khi kiểm tra toàn ánh: {str(e)}",
                'formula': formula,
            }
            return render(request, 'counting/check_surjective.html', context)
        context= {'result': is_surjective}
        return render(request=request, template_name='counting/check_surjective.html', context=context)

    def check_bijective_views(request):
        return render(request, 'counting/check_bijective.html')

    @count_data('check_bijective')
    def check_bijective_compute(request):
        domain = str(request.GET.get('domain', '')).strip()
        codomain = str(request.GET.get('codomain', '')).strip()
        mapping = f"{domain}->{codomain}"
        formula = request.GET.get('formula', '')
        if not formula or '=' not in formula:
            context = {
                'error': "Vui lòng nhập ánh xạ theo dạng 'y=x' (phải chứa '=')",
                'formula': formula,
            }
            return render(request, 'counting/check_bijective.html', context)
        result = Phuong_phap_dem()
        result.set_function(str(formula))
        try:
            is_bijective = result.check_bijective(mapping)
        except Exception as e:
            context = {
                'error': f"Lỗi khi kiểm tra song ánh: {str(e)}",
                'formula': formula,
            }
            return render(request, 'counting/check_bijective.html', context)
        context = {'result': is_bijective}
        return render(request=request, template_name='counting/check_bijective.html', context=context)

    def reverse_mapping_views(request):
        return render(request, 'counting/reverse_mapping.html')
    
    @count_data('reverse_mapping')
    def reverse_mapping_compute(request):
        domain = str(request.GET.get('domain', '')).strip()
        codomain = str(request.GET.get('codomain', '')).strip()
        mapping = f"{domain}->{codomain}"
        formula = request.GET.get('formula', '')
        if not formula or '=' not in formula:
            context = {
                'error': "Vui lòng nhập ánh xạ theo dạng 'y=x' (phải chứa '=')",
                'formula': formula,
            }
            return render(request, 'counting/reverse_mapping.html', context)
        result = Phuong_phap_dem()
        result.set_function(str(formula))
        try:
            inv_func, reverse_pairs = result.reverse_mapping(mapping)
        except Exception as e:
            context = {
                'error': f"Lỗi khi tính hàm ngược: {str(e)}",
                'formula': formula,
            }
            return render(request, 'counting/reverse_mapping.html', context)
        context={'result': f"f⁻¹(y)={inv_func}"}
        return render(request=request, template_name='counting/reverse_mapping.html', context=context)

class PigeonholeView:

    def pigeonhole_views(request):
        return render(request, 'counting/pigeonhole.html')
    
    @count_data('pigeonhole')
    def pigeonhole_compute(request):
        objects = request.GET.get('objects', '')
        pige_func = request.GET.get('pige_func', '')
        if not objects or not pige_func:
            raise ValueError("Vui lòng nhập đối tượng và hàm chuồng vào")
        new_objects = []
        for obj in objects.split(','):
            obj = obj.strip()
            if '(' in obj and ')' in obj:
                obj = obj.replace('(', '').replace(')', '')
                tuple_obj = tuple(int(x.strip()) for x in obj.split(';'))
                new_objects.append(tuple_obj)
            else:
                new_objects.append((int(obj),))

        def safe_lambda(expr: str):
            allowed_nodes = (
                ast.Expression, ast.BinOp, ast.UnaryOp,
                ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
                ast.Pow, ast.FloorDiv,
                ast.Load, ast.Name, ast.Constant,
                ast.Tuple, ast.Subscript,
            )

            tree = ast.parse(expr, mode='eval')

            for node in ast.walk(tree):
                if not isinstance(node, allowed_nodes):
                    raise ValueError("Biểu thức không hợp lệ")
            return lambda x: eval(expr, {"__builtins__": {}}, {"x": x})
        
        result = PigeonholePrinciple()
        try:
            safe_pige_func = safe_lambda(pige_func)
            holes = result.pigeonhole(tuple(new_objects), safe_pige_func)
        except Exception as e:
            context = {
                'error': f"Lỗi khi áp dụng định lí chuồng chim bồ câu: {str(e)}",
                'objects': objects,
                'pige_func': pige_func,
            }
            return render(request, 'counting/pigeonhole.html', context)
        check = False
        for hole, objs in holes.items():
            if len(objs) > 1:
                check = True
                break
        context = {
            'result': holes,
            'check': check,
            'name': 'Định lí chuồng chim bồ câu',
            'return_url': 'pigeonhole'
        }
        return render(request=request, template_name='counting/pigeonhole.html', context=context)
# Create your views here.
