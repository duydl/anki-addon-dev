import sqlite3
conn = sqlite3.connect(r"E:\Users\Radiants\Downloads\Python_code_quiz\collection.anki2")
cursor = conn.cursor()
mylist =[]

for row in cursor.execute("SELECT tags,id FROM notes"):
    b = row[1]
    a = row[0].split(" ")[1:-1]
    for i in range(len(a)):
        a[i]="Quizzes::"+a[i]
    print(a)
    a=(" "+" ".join(a)+" ",b)
    
    conn.execute('UPDATE notes SET tags= ? WHERE id = ? ', a)
 


for row in cursor.execute("SELECT tags FROM notes"):
    print(row)

conn.commit()
