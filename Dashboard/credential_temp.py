# Replace your database credentials with each below parameters


PGHOST = "The name of the host"
PGDATABASE = "The name of your Database"
PGUSER = "The name of the user"
PGPASSWORD = "The password"
PORT = "The port"
URL = "postgresql://" + PGUSER + ":" + PGPASSWORD + \
    "@" + PGHOST + ":" + PORT + "/" + PGDATABASE
