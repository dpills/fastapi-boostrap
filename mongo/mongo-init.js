db_name = "todos";
db = db.getSiblingDB(db_name);
db.createUser({
  user: "root",
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [{ role: "readWrite", db: db_name }],
});

["todos"].map((c) => db.createCollection(c));
