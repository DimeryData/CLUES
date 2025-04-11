from time import sleep  

person = 1
group = 1 

def print_receipt(serving):
    print(serving)


while person <= 5:
    print_receipt(f'Now serving person: {person}. Part of Group {group}')
    person =person+1
    sleep(1)
    if person == 5:
        print_receipt(f"Part of Group : {group}")
        person = 1
        group += 1 
        sleep(5)
