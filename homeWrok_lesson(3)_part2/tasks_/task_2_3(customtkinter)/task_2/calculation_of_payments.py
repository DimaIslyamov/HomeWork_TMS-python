def calculation_of_payments(i: float, s: float, n: int):
    p = (1 + i) ** (1/12) - 1
    m = s * p * (1 + p)**n / ((1 + p)**n - 1)

    user_total_count = m * n
    overpayment_amount = user_total_count - s

    return m, user_total_count, overpayment_amount
