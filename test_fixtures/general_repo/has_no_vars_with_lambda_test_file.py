

def function_with_lambda_as_var(number_for_test):
    result_for_main = lambda number_for_test: 2 * number_for_test
    return result_for_main


if __name__ == '__main__':
    function_with_lambda_as_var(5)
