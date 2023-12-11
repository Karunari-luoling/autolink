def read_data(conn, table, fields=None, condition=None):
    # 如果 fields 是 None 或者一个列表，将其转换为逗号分隔的字符串
    if fields is None:
        fields = '*'
    elif isinstance(fields, list):
        fields = ', '.join(fields)
    # 读取数据的 SQL 语句
    select_sql = f"SELECT {fields} FROM {table}"
    # 如果提供了条件，添加 WHERE 子句
    if condition is not None:
        select_sql += f" WHERE {condition}"
    # 执行 SQL 语句来读取数据
    cursor = conn.execute(select_sql)

    # 获取所有的数据
    rows = cursor.fetchall()
    
    # 返回数据
    return rows