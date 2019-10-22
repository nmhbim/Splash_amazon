import itertools
import re

sizeid = [
'#size_name_0',
'#size_name_1',
'#size_name_2',
'#size_name_3',
'#size_name_4',
'#size_name_5',
'#size_name_6',
'#size_name_7',
]
colorid = [
'#color_name_0',
'#color_name_1',
'#color_name_2',
'#color_name_3',
'#color_name_4',
'#color_name_5',
'#color_name_6',
'#color_name_7',
'#color_name_8',
]

fit = [
'#fit_name_0',
'#fit_name_1',
'#fit_name_2',
]

kargs = {"fit": fit, "color": colorid}
# # for commm in itertools.product(*args):
# #     print(commm)
# # string = '$19.99 - $23.99'
# string = 'https://images-na.ssl-images-amazon.com/images/I/613bYnipaZL._SR38,50_.jpg'
# # string = "The rain in Spain"
# x= string.replace('_SR38,50_', '_UL1050_')
# args['fit'].append(string)

# print(args) #this will print an object

def dunghop(**kargs):
    key = kargs.keys()
    val = kargs.values()
    aa = []
    print(key)
    print(val)
    for instance in itertools.product(*val):
        aa.append(dict(zip(key, instance)))
    return aa

aa= dunghop (**kargs)

sort_aa = aa.sort()