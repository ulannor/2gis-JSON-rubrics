import json
import pandas as pd
from treelib import Tree

def jloadfunc(filepath):
    with open(filepath, encoding='utf-8-sig') as f:
        data = json.load(f)
    return data

rubric_dict = jloadfunc(f'.\\sourcedata\\rubrics.json')
rubric_dict_2 = jloadfunc(f'.\\sourcedata\\rubrics.json')


added = set()
tree = Tree()
while rubric_dict:

    for key, value in rubric_dict.items():
        if value['parentCode'] in added:
            tree.create_node(key, key, parent=value['parentCode'])
            added.add(key)
            rubric_dict.pop(key)
            break
        elif value['parentCode'] is None:
            tree.create_node(key, key)
            added.add(key)
            rubric_dict.pop(key)
            break


paths = tree.paths_to_leaves()

lst = []
for i in paths:
    temp_dict = {}
    for el in i:
        index = i.index(el)
        code = 'code-' + str(index)
        label = 'label-' + str(index)
        temp_dict[code] = int(el)
        label_value = rubric_dict_2[str(el)]['label']
        temp_dict[label] = label_value
    temp_dict['URL_query'] = 'https://2gis.kg/bishkek/search/%20/rubricId/' + '' + str(temp_dict.get('code-3', ''))
    temp_dict['URL_query_OSH'] = 'https://2gis.kg/osh/search/%20/rubricId/' + '' + str(temp_dict.get('code-3', ''))
    lst.append(temp_dict)


df3 = pd.json_normalize(lst)

df3.sort_values(by=['code-0','code-1', 'code-2', 'code-3'], inplace=True)

print(df3)
print(type(df3))



df3.to_excel(f'.\\output\\rubrics_df_normalised.xlsx', index=False)


