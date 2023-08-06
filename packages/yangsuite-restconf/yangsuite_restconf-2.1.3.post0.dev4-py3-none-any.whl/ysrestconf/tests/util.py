def compare_dicts(expected, actual, diff=None, level=0) -> bool:
    if diff is None:
        diff = []
    actual_keys, expected_keys = sorted(actual.keys()), sorted(expected.keys())
    for key_actual, key_expected in zip(
        actual_keys, expected_keys
    ):
        if key_actual != key_expected:
            if key_actual not in expected_keys:
                return (False,
                        f"Actual value has extra property: '{key_expected}'")
            if key_expected not in actual_keys:
                return (False,
                        f"Actual value is missing property: '{key_expected}'")
        if actual[key_actual] != expected[key_expected]:
            if (not isinstance(actual[key_actual], dict) or
                    not isinstance(expected[key_expected], dict)):
                diff.insert(0, key_actual)
                return (False,
                        f"{actual[key_actual]} != {expected[key_expected]}")
            result, msg = compare_dicts(
                expected[key_expected], actual[key_actual], diff, level + 1)
            if not result:
                diff.insert(0, key_actual)
                if level == 0:
                    assert False, f"Error in {diff}\n {msg}"
                return False, msg
    return True, None
