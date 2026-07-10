import random
import string
import time

def generate_random_name(prefix="Item"):
    return f"{prefix}_{int(time.time())}"

def generate_random_code(prefix="CD"):
    return f"{prefix}_{str(int(time.time()))[-6:]}"

def generate_random_address():
    house_num = random.randint(10, 999)
    streets = ["Main St", "Broadway Ave", "Park Lane", "Link Road", "Station Road"]
    cities = ["Coimbatore", "Chennai", "Bangalore", "Mumbai"]
    return f"No. {house_num}, {random.choice(streets)}, {random.choice(cities)}"

def generate_random_postal_code():
    return "".join(["6"] + random.choices(string.digits, k=5))

def generate_random_phone():
    first_digit = str(random.choice([7, 8, 9]))
    remaining_digits = "".join(random.choices(string.digits, k=9))
    return first_digit + remaining_digits

def generate_random_email(prefix="test"):
    return f"{prefix}_{int(time.time())}@example.com"

def generate_random_description(description="Item"):
    return f"{description}_{int(time.time())}"

def generate_random_password(length=12):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "@#$%^&*!"
    
    password_char=[
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    all_pools = uppercase + lowercase + digits + special 
    password_char += random.choices(all_pools, k=length -4 )
    
    random.shuffle(password_char)
    
    return "".join(password_char)

def generate_random_unit():
    units = ["kg", "g", "mg", "L", "mL", "cm", "m", "mm", "pcs", "box", "dozen", "pair", "set", "pack"]
    return random.choice(units)