from database.connection import get_db_connection


class ReportModel:

    @staticmethod
    def get_transactions_by_period(start_date, end_date):
        conn = None
        cursor = None

        try:
            conn, cursor = get_db_connection()

            sql = """
                SELECT
                    t.id,
                    t.date_transaction,
                    t.amount,
                    t.type,
                    p.id AS product_id,
                    p.name AS product_name,
                    p.description AS product_description,
                    c.name AS contributor_name
                FROM transaction t
                INNER JOIN product p
                    ON p.id = t.id_product
                INNER JOIN contributor c
                    ON c.id = t.id_contributor
                WHERE t.date_transaction::date
                    BETWEEN %s AND %s
                ORDER BY t.date_transaction ASC, t.id ASC
            """

            cursor.execute(sql, (start_date, end_date))

            return cursor.fetchall()

        except Exception as e:
            raise Exception(str(e))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()