import json
class Compile():
# TODO Send other file
    def insert(self, table, values, returning = None):

        if 'attributes' in values:
            values['attributes'] = ','.join(['"{}" => {}'.format(k, v) if isinstance(v, (int, float)) else '"{}" => "{}"'.format(k, v) for k, v in values["attributes"].items()])
        
        if 'cond_definition' in values:
            values['cond_definition'] = ','.join(['"{}" => {}'.format(k, v) if isinstance(v, (int, float)) else '"{}" => "{}"'.format(k, v) for k, v in values["cond_definition"].items()])
        
        if not isinstance(values, list):
            values = [values]

        columns = values[0].keys()

        parameters = values[0].values()

        # value = ['(%s)' % parameters] * len(values)

        columns = ', '.join([str(x) for x in list(columns)])
        parameters = ', '.join([json.dumps(x) if isinstance(x, bool) or x is None else f"'{str(json.dumps(x))}'" if isinstance(x, dict) or isinstance(x, list) else "'{}'".format(str(x).replace("'", '"')) for x in list(parameters)])

        if returning is not None:
            return 'INSERT INTO {tablename} ({columns}) VALUES ({parameters}) returning {returning}'.format(tablename=table, columns=columns, parameters=parameters, returning=returning)
        else:
            return 'INSERT INTO {tablename} ({columns}) VALUES ({parameters})'.format(tablename=table, columns=columns, parameters=parameters)

    def update(self, table, values, conditions, returning = None):

        if 'attributes' in values:
            values['attributes'] = ','.join(['"{}" => {}'.format(k, v) if isinstance(v, (int, float)) else '"{}" => "{}"'.format(k, v) for k, v in values["attributes"].items()])
        
        columns = []
        where = []

        for key, value in values.items():
            columns.append('%s = %s' % (key, json.dumps(value) if isinstance(value, bool) or value is None else value if isinstance(value, int) or value == "null" else f"'{str(json.dumps(value))}'" if isinstance(value, dict)  or isinstance(value, list) else "'{}'".format(str(value).replace("'", '"'))))
        for key, condition in conditions.items():
                where.append('%s = %s' % (key, condition))

        columns = ', '.join([str(x) for x in list(columns)])
        where = ', '.join([str(x) for x in list(where)])

        if returning is not None:
            return ('UPDATE %s SET %s WHERE %s RETURNING %s' % (table, columns, where, returning)).strip()
        else:
            return ('UPDATE %s SET %s WHERE %s' % (table, columns, where)).strip()
    
    def delete(self, table, conditions):
        where = []
        for key, condition in conditions.items():
                where.append('%s = %s' % (key, condition))
                
        where = ', '.join([str(x) for x in list(where)])

        return ('DELETE FROM %s WHERE %s' % (table, where)).strip()

class Tools():
    def validate(self, field):
        headers = { 
                'x-status': 'FAILED',
                'x-message': 'Bad Request'
            }
        data = {'message':'The {field} field is required'.format(field=field)}
        code = 400
                
        return self.json_response(
            response=data,
            headers=headers,
            state=code
            )
