import string


low_chars = [char for char in string.ascii_lowercase]
upper_chars = [char for char in string.ascii_uppercase]
nums = [str(x) for x in range(0, 10)]

allowed_chars = low_chars + upper_chars + nums + ['_', '-']


ORDER_FOR_CONCLUSION = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
    )