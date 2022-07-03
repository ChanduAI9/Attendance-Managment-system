l=[]
with open("app.txt","r") as f:
    lines=f.readlines()


    for i in lines[1:]:

        l.append(i.split()[-1])

    print(l[0])
    k=len(l)
for i in range(k):
    if ('namburi')==l[i]:
        print("yes")
