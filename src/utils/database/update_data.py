def update_data_ignore(conn, table, fields, data, key_field):
    # 插入或忽略数据的 SQL 语句
    insert_or_ignore_sql = f"""
    INSERT OR IGNORE INTO {table} ({', '.join(fields)})
    VALUES ({', '.join(['?' for _ in fields])})
    """

    # 执行 SQL 语句来插入或忽略数据
    conn.execute(insert_or_ignore_sql, data)

    # 更新数据的 SQL 语句
    update_sql = f"""
    UPDATE {table}
    SET {', '.join([f'{field} = ?' for field in fields if field != key_field])}
    WHERE {key_field} = ?
    """

    # 执行 SQL 语句来更新数据
    conn.execute(update_sql, data[1:] + [data[0]])

    # 提交事务
    conn.commit()


def update_links_data(conn, data, mail):
    fields = ['mail', 'name', 'avatar', 'descr', 'link', 'siteshot', 'state']
    data = [mail] + data
    update_data_ignore(conn, 'links', fields, data, 'mail')

def update_friends_data(conn, data):
    fields = ['name', 'link', 'avatar']
    update_data_ignore(conn, 'friends', fields, data,'link')

def update_ban_data(conn, link):
    insert_or_ignore_sql = f"""
    INSERT OR IGNORE INTO ban (link)
    VALUES (?)
    """
    conn.execute(insert_or_ignore_sql, (link,))
    conn.commit()
