class PigeonholePrinciple:    
    def pigeonhole(self, objects: tuple, pige_func, print_log=False):
        """Phương pháp Đếm (Pigeonhole Principle)
        objects: tuple of objects to be placed into holes
        pige_func: function that maps each object to a hole
        If the pige_func function has only one parameter, put those parameters in a list, otherwise, collect the parameters into a tuple and put it in a list"""
        holes = {}
        for obj in objects:
            try:
                if isinstance(obj, tuple):
                    hole = pige_func(*obj)
                else:
                    hole = pige_func(obj)
            except TypeError as e:
                raise TypeError("Each object must be a tuple or list")
            except Exception as e:
                raise e
            if hole in holes:
                if print_log:
                    print(f"Trùng tại chuồng {hole}: {holes[hole]} và {obj}")
                holes[hole].append(obj)
            else:
                holes[hole] = [obj]
        return holes