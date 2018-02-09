

def function_with_big_complexity(list_of_items):
    result_list = []
    for item in list_of_items:
        if item:
            for k, v in item.items():
                if k:
                    if v:
                        for letter in v:
                            result_list.append(letter)
    return result_list


def function_with_small_function_with_big_complexity(list_of_items):
    result_list = []
    for item in list_of_items:
        result_list.append(item)
    return result_list


if __name__ == '__main__':

    list_of_items = [
        {
            'test_key1': ['test_val1', 'test_val2'],
            'test_key2': ['test_val3', 'test_val4'],
        },
        {
            'test_key3': ['test_val5', 'test_val6'],
            'test_key4': ['test_val7', 'test_val8'],
        },
    ]

    function_with_big_complexity(list_of_items)
    function_with_small_function_with_big_complexity(list_of_items)
