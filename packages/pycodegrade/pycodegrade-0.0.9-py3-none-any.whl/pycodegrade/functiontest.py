PYTHON_TEST_CASE = {
    'py10': {
        1: {
            'args': [(), (1, 2, 3, 4, 5, 6, 7, 8), (1, 2, 3, 4, 5)], 
            'return': [0, 8, 5],
        }, 
        2: {
            'args': ['hello my friend.', 'this IS a pen', '123123333'], 
            'return': ['HELLO MY FRIEND.', 'THIS IS A PEN', '123123333'],
        }, 
        3: {
            'args': [('sum', 0, 1, 2, 3, 4), ('mul', 1, 2, 3, 4, 5), ('mul', -1, 1, -3, 5), ('sum', -1, -2, 3, 4)],
            'return': [10, 120, 15, 4]
        }, 
        4: {
            'args': [('A+', 'A-', 'B+'), ('C', 'A+', 'B'), ('A+', 'F'), (), ('B', 'B', 'C')],
            'return': [4.0, 3.43, -1, 0, 3.03]
        }
    },
}

def get_python_testcase(uid, q):
    return PYTHON_TEST_CASE[uid.lower()][q]