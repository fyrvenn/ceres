# -*- coding: utf-8 -*-


class Config:

    @property
    def host(self):
        return '127.0.0.1'

    @property
    def port(self):
        return 8080

    @property
    def sharable_secret(self):
        return 'secret'

    @property
    def db_name(self):
        return 'db_test'

    @property
    def db_user(self):
        return 'db_user'

    @property
    def db_password(self):
        return 'db_password'

    @property
    def db_host(self):
        return '127.0.0.1'

    @property
    def db_port(self):
        return 5432

    @property
    def db_minsize(self):
        return 1

    @property
    def db_maxsize(self):
        return 10
