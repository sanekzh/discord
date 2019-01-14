import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "website.settings"
django.setup()
from django.db import connection

cursor = connection.cursor()
def print_migration(self):
    self.cursor.execute("USE db_django")
    self.cursor.execute('SHOW TABLES')
    tables = self.cursor
    sql = ''
    reverse_sql = ''
    for (table_name,) in tables:
        self.cursor.execute('SHOW fields in {}'.format(table_name))
        fields = self.cursor
        for field in fields:
            if 'varchar' in field[1] or 'text' in field[1]:
                sql += "\n 'ALTER TABLE `{}` MODIFY `{}` {} CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci ',".format(table_name, field[0], field[1])
                reverse_sql += "\n 'ALTER TABLE `{}` MODIFY `{}` {} ',".format(table_name, field[0], field[1])
    print("migrations.RunSQL(\n"
            " sql=[{}\n ],\n"
            " reverse_sql=[{}\n ]\n" "),".format(sql, reverse_sql))
