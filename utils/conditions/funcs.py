def evaluate_condition(current_price, condition):
    operator = condition[0]
    threshold = float(condition[1:])
    current_price = float(current_price)

    if operator == ">":
        return current_price > threshold
    elif operator == "<":
        return current_price < threshold
    elif operator == "=":
        return current_price == threshold
    return False

def validate_condition(condition):
    if any(operator in condition for operator in [">", "<", "="]):
        try:
            number = float(condition[1:])
            return True

        except ValueError:
            return False

    return False