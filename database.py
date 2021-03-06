import logging

import psycopg2
import psycopg2.extras

from other.config import DB_HOST, DB_NAME, DB_PASS, DB_USER
from other.utils_out import generate_bill_id


class PostSQL:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASS, host=DB_HOST
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.new_bill_id: str = generate_bill_id()

    def finish(self) -> None:
        self.cursor.close()
        self.conn.close()

    def get_all_services(self) -> list:
        try:
            self.cursor.execute('SELECT * FROM web_zalupa_servicedonate LIMIT 230')
            result = self.cursor.fetchall()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def get_service(self, service_id: int) -> dict:
        try:
            self.cursor.execute('SELECT * FROM web_zalupa_servicedonate WHERE id = %(service_id)s', {
                'service_id': service_id
            })
            result = self.cursor.fetchone()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def add_pay(self, player: str, service: str, price: int, user_id: int) -> dict:
        self.cursor.execute(
            'insert into web_zalupa_servicedonatestatus'
            '(name_player, service_id, status_pay, price, user_id_bot, time, bill_id_qiwi) '
            'values '
            '(%(player)s, %(service)s, %(status)s, %(price)s, %(user_id)s, current_timestamp, %(bill_id)s) '
            'RETURNING id',
            {
                'player': player,
                'service': service,
                'status': 'wait',
                'price': price,
                'user_id': user_id,
                'bill_id': self.new_bill_id
            }
        )
        self.conn.commit()
        result = self.cursor.fetchone()[0]
        self.finish()
        return dict(receipt_id=int(result), bill_id=self.new_bill_id)

    def get_status(self, receipt_id: int = None, bill_id: str = None) -> dict:
        try:
            if receipt_id:
                self.cursor.execute('SELECT * FROM web_zalupa_servicedonatestatus WHERE id = %(receipt_id)s', {
                    'receipt_id': receipt_id
                })
            elif bill_id:
                self.cursor.execute('SELECT * FROM web_zalupa_servicedonatestatus WHERE id = %(bill_id)s', {
                    'bill_id': bill_id
                })
            result = self.cursor.fetchone()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def update_status(self, receipt_id: int = None, bill_id: str = None, status: str = None) -> None:
        if receipt_id:
            self.cursor.execute(
                'UPDATE web_zalupa_servicedonatestatus set status_pay = %(status)s '
                'where id = %(receipt_id)s',
                {'status': status, 'receipt_id': receipt_id},
            )
        elif bill_id:
            self.cursor.execute(
                'UPDATE web_zalupa_servicedonatestatus set status_pay = %(status)s '
                'where bill_id_qiwi = %(bill_id)s',
                {'status': status, 'bill_id': bill_id},
            )
        self.conn.commit()
        self.finish()

    def get_all_settings(self) -> list:
        try:
            self.cursor.execute('SELECT * FROM web_zalupa_systemsettings')
            result = self.cursor.fetchall()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def get_banlist(self, user_id: int) -> list:
        try:
            self.cursor.execute(
                'SELECT * FROM web_zalupa_baninbot WHERE user_id = %(user_id)s',
                {'user_id': str(user_id)}
            )
            result = self.cursor.fetchall()
            self.finish()
            return result
        except Exception as e:
            logging.debug(e)

    def get_receipts(self, user_id: int) -> list:
        try:
            self.cursor.execute(
                'SELECT * FROM web_zalupa_servicedonatestatus AS z WHERE z.user_id_bot = %(user_id)s '
                'AND z.status_pay = \'wait\'',
                {
                    'user_id': int(user_id)
                }
            )
            result = self.cursor.fetchall()
            self.finish()
            return result
        except Exception as e:
            logging.error(e)

    def get_not_paid_receipts(self) -> list:
        try:
            self.cursor.execute(
                'SELECT * FROM web_zalupa_servicedonatestatus WHERE status_pay = \'wait\''
            )
            result = self.cursor.fetchall()
            self.finish()
            return result
        except Exception as e:
            logging.error(e)

    def delete_old_receipts(self) -> None:
        self.cursor.execute(
            'DELETE FROM web_zalupa_servicedonatestatus AS z WHERE z.time < NOW() - INTERVAL \'30 minutes\' '
            'AND z.status_pay = \'wait\'',
        )
        self.conn.commit()
        self.finish()

    def delete_user_not_paid_receipts(self, user_id: int) -> None:
        self.cursor.execute(
            'DELETE FROM web_zalupa_servicedonatestatus AS z WHERE z.user_id_bot = %(user_id)s '
            'AND z.status_pay = \'wait\'',
            {'user_id': user_id}
        )
        self.conn.commit()
        self.finish()
