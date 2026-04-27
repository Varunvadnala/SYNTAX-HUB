def calculator():
    num1 = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if operator == "+":
        print(f"Result: {num1 + num2}")
    elif operator == "-":
        print(f"Result: {num1 - num2}")
    elif operator == "*":
        print(f"Result: {num1 * num2}")
    elif operator == "/":
        if num2 == 0:
            print("Cannot divide by zero")
        else:
            print(f"Result: {num1 / num2}")
    else:
        print("Invalid operator")

# Loop to call function repeatedly
while True:
    calculator()
    
    choice = input("Do you want to continue? (yes/no): ").lower()
    if choice != "yes":
        print("Calculator stopped.")
        break