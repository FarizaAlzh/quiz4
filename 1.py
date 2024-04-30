import psycopg2
conn=psycopg2.connect(host="localhost",dbname="postgres",user="postgres",password="12345",port=5434)
cur=conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS person (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR
);
""")
cur.execute("""INSERT INTO person(id,name,age,gender)VALUES
(1 ,'Mike' ,25 ,'m'),
(2 ,'Jan' ,13 ,'m'),
(5 ,'Ace' ,22 ,'w');          
""")

conn.commit()
cur.close()
conn.close()