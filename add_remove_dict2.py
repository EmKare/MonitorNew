def remove_n_items(my_dict: dict, n: int):
    count = 0
    keys_to_remove = []  # Store keys to remove to avoid modifying dict during iteration

    for key in my_dict:
        if count < n:
            keys_to_remove.append(key)
            count += 1
        else:
            break

    for key in keys_to_remove:
        print(f"{key}: {my_dict[key]}")
        del my_dict[key]

    return my_dict

my_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
n = 2

result = remove_n_items(my_dict, n)
print(result)