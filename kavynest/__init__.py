# Use PyMySQL as a drop-in replacement for mysqlclient
# This is needed because Vercel's serverless environment
# doesn't support compiling C extensions (mysqlclient)
import pymysql
pymysql.install_as_MySQLdb()
