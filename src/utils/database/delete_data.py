def delete_data(conn, table, condition):
    # 删除数据的 SQL 语句
    delete_sql = f"""
    DELETE FROM {table}
    WHERE {condition}
    """

    # 执行 SQL 语句来删除数据
    conn.execute(delete_sql)

    # 提交事务
    conn.commit()

def delete_links_data(conn, mail):
    condition = f"mail = '{mail}'"
    delete_data(conn, 'links', condition)

def delete_ban_data(conn, link):
    condition = f"link = '{link}'"
    delete_data(conn, 'ban', condition)

def delete_friends_data(conn, name):
    condition = f"name = '{name}'"
    delete_data(conn, 'friends', condition)