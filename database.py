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
    if len(dicts)>0:
        return dicts
    else:
        return None


def get_all_facts(dog_id):
    return query("""SELECT CurrentDogLike, Posts.PostId, Posts.Handle, Posts.Post, dogs.Name, dogs.Bio, dogs.Age, dogs.Picture, COUNT(Likes.Handle) AS LikeCount FROM posts
INNER JOIN dogs
ON Posts.Handle = dogs.Handle
LEFT JOIN Likes
ON Posts.PostId = Likes.PostId
INNER JOIN(SELECT Posts.PostId AS PostId, COUNT(L.Handle) AS CurrentDogLike FROM Posts
LEFT JOIN (SELECT * FROM likes WHERE Handle = ?) AS L
ON Posts.PostId=L.PostId
GROUP BY Posts.PostId) AS DL
ON Posts.PostId=DL.PostId
GROUP BY Posts.PostId""", dog_id)

def get_one_dog(dog_id):
    return query("""SELECT dogs.Age, dogs.Bio, dogs.Handle, dogs.Name, dogs.Picture, Posts.Post, dogs.Password, COUNT(Likes.Handle) AS LikeCount FROM dogs
LEFT JOIN Posts
ON dogs.Handle = Posts.Handle
LEFT JOIN Likes
ON Posts.PostId = Likes.PostId
WHERE dogs.Handle = (?)
GROUP BY Likes.PostId""", (str(dog_id)))

def insert_post (handle, post_content):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
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

def create_user(username, password, name, bio, age):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    first= username
    second= password
    third= name
    fourth=bio
    fifth= age
    values=[first, second, third, fourth, fifth]

    cur.execute("""INSERT INTO dogs ([Picture], [Handle], [Password], [Name], [Bio], [Age]) VALUES('default.jpg', ?, ?, ?, ?, ?)""", values)
    conn.commit()
    conn.close()

def like_post(handle, postid):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    first= handle
    second= postid
    values=[first, second]

    cur.execute("""INSERT INTO likes ([Handle], [PostId]) VALUES( ?, ?)""", values)
    conn.commit()
    conn.close()

def unlike_post(handle, postid):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    first= handle
    second= postid
    values=[first, second]

    cur.execute("""DELETE FROM likes WHERE Handle = ? AND PostId= ? """, values)
    conn.commit()
    conn.close()

def like_count(post_id):
    conn = sqlite3.connect ('dogs.db')
    cur = conn.cursor()
    values= [post_id]
    cur.execute("""SELECT COUNT(*) FROM likes WHERE PostId = ? """, values)
    for row in cur:
        return row[0]
    