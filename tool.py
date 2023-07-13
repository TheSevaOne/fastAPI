import asyncpg
async def find_user(username):
    conn = await asyncpg.connect(user='', password='', database='', host='')
    query = ""
    password, nickname = await conn.fetchrow(query, username)
    await conn.close()
    return password, nickname


