from datetime import datetime


#===========================
# Helpers for dates in path safe mode
#===========================

def date_time_formatted():
    return datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    
def date_formatted():
    return datetime.now().strftime("%Y-%m-%d")