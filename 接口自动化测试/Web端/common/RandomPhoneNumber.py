import random

prefixes = ['13', '14', '15', '16', '17', '18', '19']
prefix = random.choice(prefixes)

suffix = ''.join(random.choices('0123456789', k=9))

phone_number = prefix + suffix
print(phone_number)

