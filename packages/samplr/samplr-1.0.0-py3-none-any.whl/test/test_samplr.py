from samplr.samplr import samplr
from samplr.errors import (
    SamplrValueError, 
    SamplrTypeError, 
    InvalidFunctionError
)
import pytest
'''
Test suite for limitr functionality and errors.
'''
def test_returns_complete_list_if_default_keyword_params():
    '''Tests that complete list is returned by the decorated function with default keyword params.'''
    dummy = ['zero', 'one', 'two', 'three', 'four']

    @samplr()
    def foo():
        return dummy
    
    sampled = foo()
    assert dummy == sampled

def test_returns_the_same_object_for_reference_types():
    '''Tests that objects returned by @limitr have the same id in memory.'''
    dummy = [{'id': 0},{'id : 1'}, {'id' : 3}]
    
    @samplr()
    def foo():
        return dummy
    
    sampled = foo()

    assert id(sampled[0]) == id(dummy[0])
    assert id(sampled[1]) == id(dummy[1])
    assert id(sampled[2]) == id(dummy[2])

def test_head_returns_first_n_items_of_list_for_positive_count():
    '''Tests that head returns the first n items from decorated function.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=3, sample_type='head')
    def foo():
        return test_list
    
    sampled = foo()
    assert sampled == ['zero', 'one', 'two']

def test_head_omits_first_n_items_of_list_for_negative_count():
    '''Test sample_type="head" works with a negative sample value.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=-3, sample_type='head')
    def foo():
        return test_list
    
    sampled = foo()
    assert sampled == ['three', 'four']

def test_tail_returns_last_n_items_of_list_for_positive_count():
    '''Tests that tail returns the last n items from decorated function.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=3, sample_type='tail')
    def foo():
        return test_list
    
    sampled = foo()
    assert sampled == ['two', 'three', 'four']

def test_tail_omits_last_n_items_of_list_for_negative_count():
    '''Tests that tail omits the last n items from decorated function.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=-3, sample_type='tail')
    def foo():
        return test_list
    
    sampled = foo()
    assert sampled == ['zero', 'one']

def test_random_returns_random_selection_from_list():
    '''Tests sample_type="random" returns randomised selection.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=3, sample_type='random')
    def foo():
        return test_list
    
    sampled = foo()

    for l in sampled:
        assert l in test_list

def test_count_bigger_than_list_length_returns_all_items():
    '''Tests count>len(<decorated list>) returns all items in decorated list.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=1000, sample_type='head')
    def foo_1():
        return test_list
    
    @samplr(count=1000, sample_type='tail')
    def foo_2():
        return test_list
    
    @samplr(count=1000, sample_type='random')
    def foo_3():
        return test_list
    
    assert foo_1() == foo_2() == foo_3()
        
def test_count_less_than_minus_list_length_returns_empty_list():
    '''Tests count< -len(<decorated list>) returns an empty list.'''
    test_list = ['zero', 'one', 'two', 'three', 'four']

    @samplr(count=-1000, sample_type='head')
    def foo_1():
        return test_list
    
    @samplr(count=-1000, sample_type='tail')
    def foo_2():
        return test_list
    
    assert foo_1() == foo_2() == []

def test_count_equals_all_returns_all_items():
    '''Tests count="all" returns all items of decorated list.'''
    dummy = ['zero', 'one', 'two', 'three', 'four']

    @samplr(sample_type='head',count='all')
    def foo_1():
        return dummy
    
    @samplr(sample_type='tail',count='all')
    def foo_2():
        return dummy
    
    @samplr(sample_type='random',count='all')
    def foo_3():
        return dummy
    
    assert foo_1() == foo_2() == foo_3() == dummy

# errors
def test_invalid_count_arg_raises_error():
    '''Tests count is type int or specified str else raises error.'''
    with pytest.raises(SamplrTypeError):
        @samplr(count='whoops')
        def foo():
            return []
        
def test_invalid_sample_type_arg_raises_error():
    '''Tests sample is a specified string else raises an error.'''
    with pytest.raises(SamplrValueError):
        @samplr(sample_type='whoops')
        def foo():
            return []
     
def test_invalid_info_arg_raises_error():
    '''Tests info is type bool else raises an error.'''
    with pytest.raises(SamplrValueError):
        @samplr(info='whoops')
        def foo():
            return []
        
def test_invalid_expand_arg_raises_error():
    '''Tests expand is type bool else raises an error.'''
    with pytest.raises(SamplrValueError):
        @samplr(expand='whoops')
        def foo():
            return []
        
def test_decorator_on_function_that_doesnt_return_list_raises_error():
    '''Tests that decorator can only decorate functions that return a list.'''
    @samplr()
    def foo():
        return 'whoops'
    
    with pytest.raises(InvalidFunctionError):
        foo()

def test_sample_type_random_with_negative_error_raises_error():
    '''Tests that a SamplrValueError is raised if sample_type=random and count<0'''
    with pytest.raises(SamplrValueError):
        @samplr(count=-3, sample_type='random')
        def foo():
            return [0,1,2,3,4,5,6,7,8,9,10]
