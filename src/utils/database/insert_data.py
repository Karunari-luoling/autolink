def insert_data_ignore(conn, table, fields, data, key_field):
    # 检查是否已经存在具有给定 key_field 值的行的 SQL 语句
    check_sql = f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE {key_field} = ?
    """
    # 执行 SQL 语句来检查是否已经存在具有给定 key_field 值的行
    count = conn.execute(check_sql, (data[0],)).fetchone()[0]
    if count == 0:
        # 如果不存在具有给定 key_field 值的行，执行插入语句
        # 插入或忽略数据的 SQL 语句
        insert_sql = f"""
        INSERT INTO {table} ({', '.join(fields)})
        VALUES ({', '.join(['?' for _ in fields])})
        """
        # 执行 SQL 语句来插入数据
        conn.execute(insert_sql, data)
    else:
        # 如果已经存在具有给定 key_field 值的行，执行更新语句

        # 更新数据的 SQL 语句
        update_sql = f"""
        UPDATE {table}
        SET {', '.join([f'{field} = ?' for field in fields if field != key_field])}, created = ?
        WHERE {key_field} = ? AND created < ?
        """
        # 执行 SQL 语句来更新数据
        conn.execute(update_sql, data[1:] + [data[fields.index('created')], data[0], data[fields.index('created')]])

    # 提交事务
    conn.commit()



def insert_links_data(conn, data, mail):
    fields = ['mail', 'name', 'avatar', 'descr', 'link', 'siteshot', 'state','created']
    data = [mail] + data
    insert_data_ignore(conn, 'links', fields, data, 'mail')

def insert_ban_data(conn, link):
    insert_or_ignore_sql = f"""
    INSERT OR IGNORE INTO ban (link)
    VALUES (?)
    """
    conn.execute(insert_or_ignore_sql, (link,))
    conn.commit()
