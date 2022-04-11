# To test

# test
ko_list = ['K07290', 'K03129', 'K02799']
result = []
for ko in ko_list:
    try:
        result.extend(get_ko_hierachy(ko))
    except:
        print(ko, 'not found')
pd.DataFrame(result, columns=['ko', 'function_def','l3', 'l2', 'l1'])
