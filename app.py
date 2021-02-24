import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="psycopgtest",
    user="postgres",
    password=123456
)
connection.set_session(autocommit=True)

# Example (This is a vulnerable system example)
# def is_admin(username: str) -> bool:
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT
#                 admin
#             FROM
#                 users
#             WHERE
#                 username = '%s'
#         """ % username)

#         result = cursor.fetchone()

#         if result is None:
#             return False

#         admin, = result
#         return admin

# print(is_admin("'; select true; --"))  # this is our attack statement
# SO as we can see, its returning true when it shouldnt.


#Correction (Now we will see the prevention of SQLi. It will return false on the same attack statement)
def is_admin(username: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                admin
            FROM
                users
            WHERE
                username = %(username)s
        """, {
            'username': username
        })

        result = cursor.fetchone()

        if result is None:
            return False

        admin, = result
        return admin

print(is_admin("'; select true; --"))

#So we saw that its working fine.