# coding=utf-8
"""
封装DBUtils
封装常用的操作
"""
import logging
from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB

logging.basicConfig()
logger = logging.getLogger("QuickDBUtils")

__all__ = [
    "SimplePolledDB",
    "SimplePersistentDB",
]


class _QuickOperate(object):
    connection = None

    def query(self, sql, *args, **kwargs):
        one = kwargs.get("one", False)
        cursor = kwargs.get('cursor', None)
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error('only <select, show, explain, desc> can be called function query()')
            raise Exception('only <select, show, explain, desc> can be called function query()')

        conn = self.connection()
        cursor = conn.cursor(cursor)
        try:
            cursor.execute(sql, args)
            if one:
                return cursor.fetchone()
            else:
                return cursor.fetchall()
        except Exception as ex:
            logger.error("query sql< {} > exception: {}".format(sql, ex))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def exec_sql(self, sql, *args, **kwargs):
        logger.debug("begin exec_sql: {}".format(sql))
        cursor = kwargs.get("cursor")
        conn = self.connection()
        cursor = conn.cursor(cursor)
        rows, last_id = None, None
        try:
            rows = cursor.execute(sql, args)
            last_id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            logger.exception("execute sql< {} >error: {}, will to rollback".format(sql, e))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return rows, last_id

    def fetchone(self, sql, *args, **kwargs):
        kwargs.update(one=True)
        return self.query(sql, *args, **kwargs)

    def fetchall(self, sql, *args, **kwargs):
        return self.query(sql, *args, **kwargs)


class SimplePolledDB(PooledDB, _QuickOperate):
    pass


class SimplePersistentDB(PersistentDB, _QuickOperate):
    pass
