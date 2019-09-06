# coding=utf-8
"""
封装DBUtils
封装常用的操作
"""
import logging
from DBUtils.PooledDB import PooledDB

logging.basicConfig()
logger = logging.getLogger("QuickDBUtils")

__all__ = [
    "SimplePolledDB",
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

    def execute(self, sql, *args, **kwargs):
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

    def executemany(self, sql, *args, **kwargs):
        logger.debug("begin exec_sql: {}".format(sql))
        cursor = kwargs.get("cursor")
        conn = self.connection()
        cursor = conn.cursor(cursor)
        rows, last_id = None, None
        try:
            rows = cursor.executemany(sql, args)
            last_id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            logger.exception("execute sql< {} >error: {}, will to rollback".format(sql, e))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return rows, last_id

    def exec_sql(self, sql, *args, **kwargs):
        return self.execute(sql, *args, **kwargs)

    def fetchone(self, sql, *args, **kwargs):
        kwargs.update(one=True)
        return self.query(sql, *args, **kwargs)

    def fetchall(self, sql, *args, **kwargs):
        return self.query(sql, *args, **kwargs)

    def fetchmany(self, sql, *args, **kwargs):
        size = kwargs.get("size", 30)
        cursor = kwargs.get('cursor', None)
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error('only <select, show, explain, desc> can be called function query()')
            raise Exception('only <select, show, explain, desc> can be called function query()')

        conn = self.connection()
        cursor = conn.cursor(cursor)
        try:
            cursor.execute(sql, args)
            while True:
                tmp = cursor.fetchmany(size)
                if not tmp:
                    break
                for item in tmp:
                    yield item
        except Exception as ex:
            logger.error("query sql< {} > exception: {}".format(sql, ex))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


class SimplePolledDB(PooledDB, _QuickOperate):
    pass
