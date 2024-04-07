import os
import sqlite3

def create_database():
    # 创建数据库
    root_dir = os.path.abspath('.')
    conn = sqlite3.connect(os.path.join(root_dir,"data","autolink.db"), check_same_thread=False)
    # 创建表的 SQL 语句
    create_table_sqls = {
        "links": """
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mail TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                avatar TEXT NOT NULL,
                descr TEXT NOT NULL DEFAULT 这个人还没有介绍哦,
                link TEXT NOT NULL,
                siteshot TEXT,
                state INTEGER NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                message_id TEXT
            )
        """,
        "ban": """
            CREATE TABLE IF NOT EXISTS ban (
                link TEXT PRIMARY KEY
            )
        """,
        "feishu_token": """
            CREATE TABLE IF NOT EXISTS feishu_token (
                token TEXT,
                expire integer
            )
        """
    }

    # 在循环中执行 SQL 语句来创建表
    for table_name ,create_table_sql in create_table_sqls.items():
        conn.execute(create_table_sql)

    # 关闭数据库连接
    conn.close()

def check_and_create_database():
    root_dir = os.path.abspath('.')
    db_path = os.path.join(root_dir,"data","autolink.db")
    if not os.path.exists(db_path):
        create_database()
    return db_path