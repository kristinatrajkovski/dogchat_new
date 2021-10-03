import sqlite3


def query(query_text, *param):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    cur.execute(query_text, param)

    column_names = []
    for column in cur.description:
        column_names.append(column[0])

    print(column_names)
    rows = cur.fetchall()

    dicts= []
    for row in rows:
        d = dict(zip(column_names, row))
        dicts.append(d)
    conn.close()
    return dicts


def get_all_facts():
    return query("""SELECT Posts.PostId, Posts.Handle, Posts.Post, dogs.Name, dogs.Bio, dogs.Age, dogs.Picture, COUNT(Likes.Handle) AS LikeCount FROM posts
INNER JOIN dogs
ON Posts.Handle = dogs.Handle
LEFT JOIN Likes
ON Posts.PostId = Likes.PostId
GROUP BY Posts.PostId
ORDER BY Posts.PostId""")

def get_one_dog(dog_id):
    return query("""SELECT dogs.Age, dogs.Bio, dogs.Handle, dogs.Name, dogs.Picture, Posts.Post, COUNT(Likes.Handle) AS LikeCount FROM dogs
INNER JOIN Posts
ON dogs.Handle = Posts.Handle
LEFT JOIN Likes
ON Posts.PostId = Likes.PostId
WHERE dogs.Handle = (?)
GROUP BY Likes.PostId""", (str(dog_id)))

def insert_post (handle, post_content):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    first= handle
    second= post_content
    values=[handle, post_content]

    cur.execute("""INSERT INTO Posts ([PostId], [Handle], [Post]) VALUES(NULL, ?, ?)""", values)
    conn.commit()
    conn.close()

def delete_post(post_id):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    cur.execute("""DELETE FROM Posts WHERE PostId= ?""", post_id)
    conn.commit()
    conn.close()