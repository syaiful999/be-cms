
def queryStringGenerator(params):
  queryReturn = ''
  for field in params:
    qParamsValue = params[field].split('|')
    value = qParamsValue[0]
    typeData = qParamsValue[1]
    operator = qParamsValue[2]
    print(value, typeData, operator)
    continue
  return queryReturn

def stringGenerator(value, operator):
  return ''

def numericGenerator(value, operator):
  return ''

def dateGenerator(value, operator):
  return ''
