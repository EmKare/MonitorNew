a = [3,4,5,6,7,8,9,]
b = [0,1,2,]

def yes_no():
    global a,b
    while True:
        print(f"len a: {len(a)}: {[x for x in a]}")
        print(f"len b: {len(b)}: {[x for x in b]}")
        print()
        ans = int(input("y = 1/n = 0: "))
        if ans:
            amt = int(input("how many: "))
            move_item(amt)
        else:
            break
        
def move_item(amt: int):
    global a,b
    start = 0
    while amt > 0:
        move = a[start]
        b.append(move)
        a.remove(move)
        
        amt -= 1

yes_no()