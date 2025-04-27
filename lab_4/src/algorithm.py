def luhn(number: int) -> int:
    rev_dig = map(int, reversed(str(number)))

    summ = 0

    for idx, number in enumerate(rev_dig):
        if idx % 2 == 0:
            number *= 2
            summ += number - 9 if number > 9 else number
        else:
            summ += number

    summ %= 10

    control = (10 - summ) % 10

    return control


def card_is_correct(
    card: str
) -> bool:
    if len(card) != 16:
        return False

    last = int(card[-1])
    control = luhn(int(card[:-1]))

    return control == last


if __name__ == "__main__":
    print(card_is_correct("2202202355549834"))
    # num = 853
    # print(list(enumerate(map(int, reversed(str(num))))))