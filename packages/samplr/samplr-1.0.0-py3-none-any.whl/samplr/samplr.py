'''
◆   ◇   ◆   S A M P L R   ◆   ◇   ◆

Samplr is a lil decorator which can take a lil sample
of items from a decorated function's returned list.

Example use:

@samplr(count=3)
def this_func_returns_a_list():
    ...
    return my_list
'''
import json
from random import sample as random_sample
from typing import Tuple
from samplr.errors import (
    SamplrValueError, 
    SamplrTypeError, 
    InvalidFunctionError
)
from samplr.strings import (
    header,
    footer,
    err_msg
)

def samplr(
        count : str | int  = 'all',
        sample_type : str = 'head',
        expand : bool = True,
        info : bool = True,
    ) -> list:
    '''
    Decorate a function which returns a list with @samplr() to instead
    return a new list containing a fewer number of items.


    

    Parameters:


    '''
    if type(count) != int:
        if count !='all':
            raise SamplrTypeError(err_msg(0))
    elif sample_type == 'random' and count < 0:
        raise SamplrValueError(err_msg(5))

    valid_sample_types = ['head', 'tail', 'random']
    if sample_type not in valid_sample_types:
        raise SamplrValueError(err_msg(1, ", ".join(valid_sample_types)))
    
    if type(info) != bool:
        raise SamplrValueError(err_msg(2))
    
    if type(expand) != bool:
        raise SamplrValueError(err_msg(3))
    
    def wrapper_2(func):
        def wrapper_1():
            nonlocal count

            output = func()
            if not isinstance(output, list):
                raise InvalidFunctionError(err_msg(4, func.__name__))
            
            if count == 'all':
                count = len(output)
            elif count > len(output):
                count = len(output)
            elif count < -len(output):
                count = 0

            if info:
                print(header(
                    func.__name__,
                    count, 
                    output, 
                    sample_type,
                    expand,
                    info
                )
            )

            sample_data = eval(f'_select_{sample_type}(output, count)')
            sampled_items = sample_data[0]
            indices = sample_data[1]
            sampled_count = len(sampled_items)

            entries = []
            for i in range(0, sampled_count):
                idx = _create_idx_prefix(indices[i], sampled_count)
                entry = sampled_items[i] if not expand else json.dumps(
                    sampled_items[i], 
                    indent = 4, 
                    default = str)  
                entries.append(f'{idx}: {entry}')
            
            for entry in entries:
                separator = ',\n' if '\n' in entry else '\n'
                print(entry, sep=separator)

            if info:
                print(footer())

            return sampled_items
        return wrapper_1
    return wrapper_2

def _select_head(list : int, count : int) -> Tuple[list, list]:
    if count<0:
        total_items = len(list)
        start = abs(count)
        return list[start:], range(start, total_items+1)
    else:
        return list[:count], range(0, count+1)

def _select_tail(list : int, count : int) -> Tuple[list, list]:
    if count == 0:
        return [],[]
    total_items = len(list)
    if count<0:
        return list[0:count], range(0, total_items+count)
    else:
        return list[-count:], range(total_items-count,total_items)

def _select_random(list : int, count : int) -> Tuple[list, list]:
    random_indices = random_sample(range(0,len(list)), k=count)
    sorted_indices = sorted(random_indices)
    random_items = []

    for i in sorted_indices:
        random_items.append(list[i])
    return random_items, sorted_indices

def _create_idx_prefix(idx : int, sampled_count : int) -> str:
    int_string = str(idx)
    max_int_str = str(sampled_count)
    spaces_to_add = (len(max_int_str) - len(int_string))*' '
    idx_string =  spaces_to_add + int_string
    diamond = '◇' if idx % 2 == 0 else '◆'
    return f'\u001B[30m{diamond} {idx_string}: \u001B[0m'
