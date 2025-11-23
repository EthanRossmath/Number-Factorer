from typing import List, Tuple

def consolidate_pairs(factor_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Takes a list of pairs of integers [(a_1,n_1), ..., (a_k, n_k)] and consolidates
        them so that the first entries are unique.
        """
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