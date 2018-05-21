# -*- coding: utf-8 -*-


async def authenticate(engine, username, password):
    """
    The function checks if there is a username with such password exists in the database.

    We assume that the password was created by following algorithm:

    ``` python
    import hashlib, uuid
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    db_password = hashed_password + ':' + salt
    ```

    :param engine: aiopg.sa.Engine instance
    :param username: str
    :param password: str
    :return: dictionary {id, name, role} or None
    """
    raise NotImplementedError()


async def list_users(engine, offset=0, limit=5):
    """
    Function returns a list of users from a data source.

    :param engine: aiopg.sa.Engine instance
    :param offset: integer offset of the list of users
    :param limit: maximum number of records to return
    :return: a list of user objects
    """
    return []
