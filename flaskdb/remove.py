from models import get_db_connection

def delete_category(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM subcategories WHERE id = ?', (id,))
    conn.commit()
    conn.close()

delete_category(1)

# for i in range(15):
#     delete_category(i+2)