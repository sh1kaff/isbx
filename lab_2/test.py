from src.utils import get_bits
from src.tests.frequency_bit_test import frequency_bit_test
from src.tests.next_bit_test import next_bit_test
from src.tests.longest_run_test import longest_run_test128

def main():
    bits = get_bits("cpp")
    print(bits)

    print(
        frequency_bit_test(bits)
    )

    print(
        next_bit_test(bits)
    )

    print(
        longest_run_test128(bits)
    )

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)