import random 

def get_payment_status():
    randon_number = random.random()  
    if randon_number < 0.8:
        return "successful"
    else:
        return "rejected"