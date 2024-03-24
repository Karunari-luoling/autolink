def update_links_data(conn, data):
    fields = ['mail', 'name', 'avatar', 'descr', 'link', 'siteshot', 'state', 'created']
    mail = data['mail']
    update_fields = ', '.join(f'{field} = ?' for field in fields if field in data)
    update_values = [data[field] for field in fields if field in data]
    conn.execute(f"UPDATE links SET {update_fields} WHERE mail = ?", update_values + [mail])
    conn.commit()