def calculation_of_payments(*, interest_rate: float, loan_amount: float, months_count: int):
    monthly_interest_rate = (1 + interest_rate) ** (1 / 12) - 1

    monthly_payment = (loan_amount * monthly_interest_rate
                       * (1 + monthly_interest_rate) ** months_count
                       / ((1 + monthly_interest_rate) ** months_count - 1))

    user_total_count = monthly_payment * months_count
    overpayment_amount = user_total_count - loan_amount

    return monthly_payment, user_total_count, overpayment_amount
