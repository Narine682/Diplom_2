import random
import string

def random_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=6))}@example.com"

