# coding: utf-8
def normalize_sql(sql, *_, **kwargs):
    """格式化sql"""
    sql = ' '.join(sql.split('\n'))
    sql = ' '.join(sql.split())
    return sql.format(sql, **kwargs)
