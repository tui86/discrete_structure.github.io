from django.shortcuts import render
from .relation_core import Relationship
from .models import RelationModel
from functools import wraps
import json
# Create your views here.

def count_relation_data(name):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                counter, _ = RelationModel.objects.get_or_create(name=name)
                counter.count += 1
                counter.save()
            except Exception:
                pass  # không cho thống kê làm chết web
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def convert_str_to_tuple_list(input_str):
    if not input_str:
        raise ValueError("Input string is empty")
    if ')(' in input_str:
        raise ValueError("Invalid format: missing space between tuples")
    tuple_list = []
    pairs = input_str.split(' ')
    for pair in pairs:
        pair = pair.replace('(', '').replace(')', '')
        elements = pair.split(',')
        if len(elements) == 2:
            try:
                first_elem = int(elements[0].strip())
                second_elem = int(elements[1].strip())
                tuple_list.append((first_elem, second_elem))
            except ValueError:
                continue
    return tuple_list

def convert_string_to_int_list(input_str):
    if not input_str:
        raise ValueError("Input string is empty")
    for i in input_str:
        if not (i.isdigit() or i == ','):
            raise ValueError("Input string contains invalid characters")
    str_list = input_str.split(',')
    int_list = []
    for item in str_list:
        try:
            int_list.append(int(item.strip()))
        except ValueError:
            continue
    return int_list

class RelationshipViews:
    def plus_and_minus_modulo_views(request):
        return render(request, 'relation/plus_and_minus_modulo.html')
    
    @count_relation_data('plus_and_minus_modulo')
    def plus_and_minus_modulo_compute(request):
        var_a = request.GET.get('a','')
        var_b = request.GET.get('b','')
        var_c = request.GET.get('c','')
        var_d = request.GET.get('d','')
        modulo = request.GET.get('modulo','')
        if modulo == '+':
            try:
                relation = Relationship.Modulo()
                result = relation.plus_modulo(int(var_a), int(var_c), int(var_b), int(var_d))
            except Exception as e:
                context = {
                    'error': f"Lỗi khi tính toán biểu thức, vui lòng kiểm tra lại biểu thức"
                }
                return render(request, 'relation/plus_and_minus_modulo.html', context)
            context = {
                'a':var_a,
                'b':var_b,
                'c':var_c,
                'd':var_d,
                'modulo':modulo,
                'result':result
            }
            return render(request, 'relation/plus_and_minus_modulo.html', context)
        elif modulo == '-':
            try:
                relation = Relationship.Modulo()
                result = relation.minus_modulo(int(var_a), int(var_c), int(var_b), int(var_d))
            except Exception as e:
                context = {
                    'error': f"Lỗi khi tính toán biểu thức, vui lòng kiểm tra lại biểu thức"
                }
                return render(request, 'relation/plus_and_minus_modulo.html', context)
            context = {
                'a':var_a,
                'b':var_b,
                'c':var_c,
                'd':var_d,
                'modulo':modulo,
                'result':result
            }
            return render(request, 'relation/plus_and_minus_modulo.html', context)
        else:
            context = {
                'error': "Vui lòng nhập đầy đủ dữ liệu và chọn phép tính hợp lệ"
            }
            return render(request, 'relation/plus_and_minus_modulo.html', context)
        
    def multiple_modulo_views(request):
        return render(request, 'relation/multiple_modulo.html')
    
    @count_relation_data('multiple_modulo')
    def multiple_modulo_compute(request):
        var_a = request.GET.get('a','')
        var_b = request.GET.get('b','')
        var_c = request.GET.get('c','')
        var_d = request.GET.get('d','')
        try:
            relation = Relationship.Modulo()
            result = relation.multiple_modulo(int(var_a), int(var_c), int(var_b), int(var_d), print_log=False)
        except Exception as e:
            context = {'error': "Lỗi khi tính toán biểu thức, vui lòng kiểm tra lại biểu thức"}
            return render(request, 'relation/multiple_modulo.html', context)
        context = {
                'a':var_a,
                'b':var_b,
                'c':var_c,
                'd':var_d,
                'result':result
            }
        return render(request, 'relation/multiple_modulo.html', context)
    
    def exponential_modulo_views(request):
        return render(request, 'relation/exponential_modulo.html')
    
    @count_relation_data('exponential_modulo')
    def exponential_modulo_compute(request):
        var_a = request.GET.get('a','')
        var_b = request.GET.get('b','')
        var_m = request.GET.get('m','')
        try:
            relation = Relationship.Modulo()
            result = relation.exponential_modulo(int(var_a), int(var_b), int(var_m))
        except Exception as e:
            context = {
                'error': "Lỗi khi tính toán biểu thức, vui lòng kiểm tra lại biểu thức"
            }
            return render(request, 'relation/exponential_modulo.html', context)
        context = {
            'a': var_a,
            'b': var_b,
            'm': var_m,
            'result': result
        }
        return render(request, 'relation/exponential_modulo.html', context)

    def check_the_properties_of_the_relationship_views(request):
        return render(request, 'relation/check_the_properties_of_the_relationship.html')
    
    @count_relation_data('check_the_properties_of_the_relationship')
    def check_the_properties_of_the_relationship_compute(request):
        relationship = request.GET.get('relationship','')
        background_relationship  = request.GET.get('background_relationship','')
        operator = request.GET.get('operator','')
        expression = request.GET.get('expression','')
        try:
            relation = Relationship()
            if relationship:
                relation.set_relationship(convert_str_to_tuple_list(relationship))
            else:
                relation.create_operator_relationship(convert_string_to_int_list(background_relationship), operator)
            
            match expression:
                case 'reflective':
                    result = relation.check_reflective_relationship()
                case 'symmetric':
                    result = relation.check_symmetrical_relationship()
                case 'transitive':
                    result = relation.check_bridging_relationship()
                case 'equivalence':
                    result = relation.check_equivalent_relationship()
                case 'antisymmetric':
                    result = relation.check_antisymmetric_relationship()
                case 'partial_order':
                    result = relation.check_order_relationship()
                case 'total_order':
                    result = relation.check_total_order_relationship()
                case _:
                    context = {
                        'error': "Vui lòng chọn tính chất quan hệ hợp lệ"
                    }
                    return render(request, 'relation/check_the_properties_of_the_relationship.html', context)
        except Exception as e:
            context = {
                'error': f"Lỗi khi kiểm tra tính chất quan hệ, vui lòng kiểm tra lại biểu thức"
            }
            return render(request, 'relation/check_the_properties_of_the_relationship.html', context)
        
        context = {
            'relationship': relationship,
            'background_relationship': background_relationship,
            'operator': operator,
            'expression': expression,
            'result': result
        }
        return render(request, 'relation/check_the_properties_of_the_relationship.html', context)
    
    def create_hasse_diagram_views(request):
        return render(request, 'relation/create_hasse_diagram.html')
    
    @count_relation_data('create_hasse_diagram')
    def create_hasse_diagram_compute(request):
        relationship = request.GET.get('relationship','')
        background_relationship  = request.GET.get('background_relationship','')
        operator = request.GET.get('operator','')
        try:
            relation = Relationship()
            if relationship:
                relation.set_relationship(convert_str_to_tuple_list(relationship))
                nodes = relation.background_relationship
            else:
                relation.create_operator_relationship(convert_string_to_int_list(background_relationship), operator)
                # Sử dụng powerset khi operator liên quan đến subset
                if operator in ['subset', 'proper subset', 'superset', 'proper superset']:
                    nodes_set = relation.powerset
                    # Tạo mapping từ frozenset sang string representation
                    node_map = {subset: '{' + ', '.join(map(str, sorted(subset))) + '}' for subset in nodes_set}
                    nodes = list(node_map.values())
                else:
                    nodes = relation.background_relationship
                    node_map = {n: str(n) for n in nodes}
            edges = relation.create_hasse_diagram()
        except Exception as e:
            context = {
                'error': f"Lỗi khi tạo biểu đồ Hasse, vui lòng kiểm tra lại biểu thức"
            }
            return render(request, 'relation/create_hasse_diagram.html', context)
        
        elements = []
        for n in nodes:
            elements.append({'data': {'id':str(n), 'label':str(n)}})

        for u, v in edges:
            # Map frozenset/int về string representation
            if operator in ['subset', 'proper subset', 'superset', 'proper superset']:
                source = node_map.get(u, str(u))
                target = node_map.get(v, str(v))
            else:
                source = str(u)
                target = str(v)
            elements.append({
                'data':
                {
                    'source': source,
                    'target': target
                }
            })

        return render(request, 'relation/create_hasse_diagram.html', {'elements': json.dumps(elements)})