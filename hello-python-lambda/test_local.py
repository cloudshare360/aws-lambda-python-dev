from app import lambda_handler

if __name__ == "__main__":
    event = {"name": "Sri"}
    context = {}  # You can create a mock context object if needed

    response = lambda_handler(event, context)
    print("Lambda Output:", response)
