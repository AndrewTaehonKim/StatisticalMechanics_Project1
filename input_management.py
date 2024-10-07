def read_input(input_file):
    input_data = {}
    with open(input_file, 'r') as f:
        for line in f.read().splitlines():
            key, value = line.split()
            input_data[key] = float(value)
    # Assertions to check if the required keys are present
    assert 'u' in input_data, "Missing 'u' in input data"
    assert 'V' in input_data, "Missing 'V' in input data"
    assert 'T' in input_data, "Missing 'T' in input data"
    # ADD 1 Mole as N
    input_data['N'] = 6.022e23
    # molar mass g/mol -> kg/mol ... used as mass basically
    input_data['u'] /= 1e3
    # volume of gas L -> m^3
    input_data['V'] /= 1e3
    return input_data