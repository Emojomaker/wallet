import datetime

def log(message):
    date = datetime.datetime.now()
    with open('log_operations', 'a') as file:
        file.write(str(date)+': '+ str(message)+'\n')
