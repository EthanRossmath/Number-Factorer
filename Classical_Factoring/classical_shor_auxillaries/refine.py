def consolidate_pairs(factor_list: list):
    combine_dict = {}
    for a in factor_list:
        if a[0] in combine_dict:
            combine_dict[a[0]] += a[1]
        else:
            combine_dict[a[0]] = a[1]
    combine_list = []
    for a in combine_dict:
        combine_list.append((a, combine_dict[a]))
    
    combine_list.sort(key=lambda x: x[0])
    return combine_list