import json


class JsonQuery:

    def __init__(self, json_str=None):

        if not json_str:
            raise Exception('Passed json string is empty')
        else:
            self.obj_list = json.loads(json_str)
            self.obj_type = type(self.obj_list)

    def count(self):
        return len(self.obj_list)

    def first(self):
        if self.obj_type == dict:
            return self.obj_list
        elif self.obj_type == list:
            return self.obj_list[0]

    def last(self):
        if self.obj_type == dict:
            return self.obj_list
        elif self.obj_type == list:
            return self.obj_list[-1]

    def eq(self, lhs, rhs):
        return lhs == rhs

    def neq(self, lhs, rhs):
        return lhs != rhs

    def gt(self, lhs, rhs):
        return lhs > rhs

    def gte(self, lhs, rhs):
        return lhs >= rhs

    def lt(self, lhs, rhs):
        return lhs < rhs

    def lte(self, lhs, rhs):
        return lhs <= rhs

    def startswith(self, lhs, rhs):
        return lhs.startswith(rhs)

    def istartswith(self, lhs, rhs):
        lhs = lhs.lower()
        rhs = rhs.lower()

        return lhs.startswith(rhs)

    def endswith(self, lhs, rhs):
        return lhs.endswith(rhs)

    def iendswith(self, lhs, rhs):
        lhs = lhs.lower()
        rhs = rhs.lower()

        return lhs.endswith(rhs)

    def contains(self, lhs, rhs):
        return rhs in lhs

    def icontains(self, lhs, rhs):
        lhs = lhs.lower()
        rhs = rhs.lower()

        return rhs in lhs

    def eval_operation(self, obj, key, operation):
        value = operation.pop(-1)

        if len(operation) == 1:
            operator = operation[0]

            if operator == 'eq':
                return self.eq(obj[key], value)
            elif operator == 'neq':
                return self.neq(obj[key], value)
            elif operator == 'gt':
                return self.gt(obj[key], value)
            elif operator == 'gte':
                return self.gte(obj[key], value)
            elif operator == 'lt':
                return self.lt(obj[key], value),
            elif operator == 'lte':
                return self.lte(obj[key], value)
            elif operator == 'startswith':
                return self.startswith(obj[key], value)
            elif operator == 'istartswith':
                return self.istartswith(obj[key], value)
            elif operator == 'endswith':
                return self.endswith(obj[key], value)
            elif operator == 'iendswith':
                return self.iendswith(obj[key], value)
            elif operator == 'contains':
                return self.contains(obj[key], value)
            elif operator == 'icontains':
                return self.icontains(obj[key], value)

    def apply_operations(self, operation_dict):

        result = []
        for obj in self.obj_list:
            total_operation = len(operation_dict)

            for index, (key, operation) in enumerate(operation_dict.items()):
                if not self.eval_operation(obj, key, list(operation)):
                    break
                elif total_operation == index + 1:
                    result.append(obj)

        return result

    def generate_operation_dict(self, **kwargs):

        operation_dict = {}
        for k, v in kwargs.items():
            key_op_list = k.split('__')

            if len(key_op_list) == 1:
                operation = ['eq']
            else:
                if key_op_list[-1] == '':
                    key_op_list.pop(-1)
                operation = key_op_list[1:]

            operation.append(v)
            operation_dict[key_op_list[0]] = operation

        return operation_dict

    def get(self, **kwargs):
        operation_dict = self.generate_operation_dict(**kwargs)
        result = self.apply_operations(operation_dict)

        if len(result) > 1:
            raise Exception('Get returned more than 1 result')
        else:
            return result[0]

    def filter(self, **kwargs):
        operation_dict = self.generate_operation_dict(**kwargs)
        result = self.apply_operations(operation_dict)
        return result
