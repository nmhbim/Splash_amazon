import itertools

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

fitid = [
'#fit_name_0',
'#fit_name_1',
'#fit_name_2',
'#fit_name_3',
]

args = [fitid, colorid, sizeid]

for commm in itertools.product(*args):
    print(commm)
