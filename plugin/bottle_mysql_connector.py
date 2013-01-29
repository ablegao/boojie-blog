#coding:utf-8
'''

Usage Example::

    import bottle
    import bottle_mysql_connector

    app = bottle.Bottle()
    # dbhost is optional, default is localhost
    plugin = bottle_mysql.Plugin(username='user', password='pass', database='db')
    app.install(plugin)

    @app.route('/show/:<tem>')
    def show(item, db):
        db.execute('SELECT * from items where name="%s"', (item,))
        row = db.fetchone()
        if row:
            return template('showitem', page=row)
        return HTTPError(404, "Page not found")
'''

__author__ = "Able Gao"
__version__ = '0.1.1'
__license__ = 'MIT'

### CUT HERE (see setup.py)

import inspect
import mysql.connector
from mysql.connector import errorcode
from bottle import HTTPResponse, HTTPError,PluginError


class MySQLConnectorPlugin(object):
    '''
    This plugin passes a mysql database handle to route callbacks
    that accept a `db` keyword argument. If a callback does not expect
    such a parameter, no connection is made. You can override the database
    settings on a per-route basis.
    '''

    name = 'mysql'

    def __init__(self, user="" , password='' , host='' , port=3306 , database=None ,keyword='db' ,autocommit = True):
        self.user       = user
        self.password   = password
        self.host       = host
        self.port       = port
        self.database   = database
        self.keyword    = keyword
        self.autocommit = autocommit
    def setup(self, app):
        '''
        Make sure that other installed plugins don't affect the same keyword argument.
        '''
        for other in app.plugins:
            if not isinstance(other, MySQLConnectorPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another mysql plugin with conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        mysql_conf ={}
        conf                        = context['config'].get('mysql') or {}
        mysql_conf['database']      = conf.get('database' , self.database)
        mysql_conf['user']          = conf.get("user" , self.user)
        mysql_conf['password']      = conf.get("password" , self.password)
        mysql_conf['port']          = conf.get("port" ,     self.port)
        mysql_conf['host']          = conf.get("host",      self.host)
        mysql_conf['autocommit']    = conf.get("autocommit",      self.autocommit)
        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        args = inspect.getargspec(context['callback'])[0]
        if self.keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the database
            con = None
            try:
                # Using DictCursor lets us return result as a dictionary instead of the default list
                
                con     = mysql.connector.MySQLConnection(**mysql_conf)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    raise HTTPError("Something is wrong your username or password",err)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    raise HTTPError("Database does not exists",err)
                else:
                    raise HTTPError(err)
                con.close()
                return None
            except HTTPResponse as err:
                raise HTTPError(500, "Database Error", err)
            cursor = con.cursor()
            # Add the connection handle as a keyword argument.
            kwargs[self.keyword] = cursor

            try:
                rv = callback(*args, **kwargs)
            except HTTPError as  e:
                raise
            except HTTPResponse as e:
                raise
            finally:
                if con:
                    con.close()
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper

Plugin = MySQLConnectorPlugin
