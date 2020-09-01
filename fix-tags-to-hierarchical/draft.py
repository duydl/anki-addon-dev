import sqlite3

def fix_tag(path, parent_tag):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    mylist =[]
    for row in cursor.execute("SELECT tags,id FROM notes"):
        b = row[1]
        a = row[0].split(" ")[1:-1]
        for i in range(len(a)):
            a[i]=  parent_tag + "::" + a[i]
        print(a)
        a=(" "+" ".join(a)+" ",b)
        
        conn.execute('UPDATE notes SET tags= ? WHERE id = ? ', a)
    


    for row in cursor.execute("SELECT tags FROM notes"):
        print(row)

    conn.commit()

fix_tag(r"E:\Users\Radiants\Desktop\Knack__Who Composed Me_\collection.anki2","Compose")