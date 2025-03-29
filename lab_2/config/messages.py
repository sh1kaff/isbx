ERRORS = {
    "empty_bit_string": "Bit string is empty",
    "invalid_bits_len": "The length of the bit string should be 128",
    "invalid_char_in_bits": "The string should only consist of '0' and '1'",
    "invalid_path": "Path {path} is invalid",
    "invalid_lang": "Lang {lang} is invalid",
    "invalid_test": "Test {test} is invalid"
}


NAMES = {
    "exe_file_name": "gen_{lang}.exe",
    "java_file_name": "Gen.class"
}


MESSAGES = {
    "what_lang": "Lang for generating: {lang}",
    "bits_result": "Generated bits string: {bits}",
    "test_result": "Result of {test} test: P_value = {result}",
    "status": "Status: {status}"
}


DESCRIPTIONS = {
    "program": "Generates a sequence of bits and tests it for randomness using NIST tests.",
    "gen_lang": "Languages for sequence generation.",
    "tests": "Available randomization tests. Do not specify anything to invoke all tests."
}
