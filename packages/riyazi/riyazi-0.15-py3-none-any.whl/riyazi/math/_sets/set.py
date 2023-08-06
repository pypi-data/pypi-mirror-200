def complement(U,A):
    return U-A

def difference(A,B):
    """ 
    >>> difference({1,2,3,4,5,6},{2,4,6,8})
    
    """
    print(type(A))
    print(type(B))
    if(type(A) ==type({dict})  and type(B) == type({dict})):
        
        return type((A-B))
    else:
        print("Enter both set value  data type")

def intersection(l1, l2):
    temp = []

    for item in l1:
        if item in l2 and item not in temp:
            temp.append(item)

    return temp

def power_set(s):

    power_set = [set()]

    for element in s:
        one_element_set = {element}
        power_set += [subset | one_element_set for subset in power_set]

    return power_set

def symmetric(A,B):
    """symmetric"""
    print(type(A))
    print(type(B))

    if(type(A) ==type(set)  and type(B) == type({set})):
        return A^B
    else:("enter both  set data type ")


def union(lists):
    
    all_elements = []
    for x in lists:
        all_elements = all_elements + x
    return set(set(all_elements))