# CRUD Overview

_Basics of Schema Design_  
_Modeling relationships_

---

## Common Read commands

- **\l** -> lists all dbs
- **\dt** -> lists all tables in curr db
- **\d table_name** -> lists table data from within db

---

## Creating and dropping a new db

```sql
-- from linux terminal without connecting to anything
createdb new-db
dropdb new-db
-- from within pysql shell / seed file
- CREATE DATABASE new_db
- DROP DATABASE new_db
```

---

# DDL and Schema Design

## DB Initialization

```sql
 DROP DATABASE IF EXISTS example_db;
 CREATE DATABASE example_db;
 \c example_db;
```

## Table Structure

```sql
CREATE TABLE name (
  id SERIAL PRIMARY KEY,
  title TEXT,
  price FLOAT,
  page-count INTEGER
);
```

_Check sql-ddl-demo/example.sql_

---

## Column Data types

## [PGSQL Docs on Data Types](https://www.postgresql.org/docs/12/datatype.html)

---

## Special Considerations

---

### NULL

NULL is special value for 'unknown'/'none' -- not 0 or ''  
We cannot select rows base on 'data = NULL' instead we check 'data IS NULL'  
**This is a bit of a pain so generally, we want as few null values as possible-**

---

## Conversions

---

SQL will convert floats when passed to an int;
SQL will convert nums in general to text;

## Constraints

---

When defining a particular table, we can specify constraints on columns:

`PRIMARY KEY`  
`UNIQUE` - verify data is non-duplicating  
`NOT NULL` - prevent null  
`CHECK` - can define condtional logic  
`FOREIGN KEY`

## Examples

```
CREATE TABLE users (
id SERIAL PRIMARY KEY,
phone_number TEXT UNIQUE,
password TEXT NOT NULL,
account_balance FLOAT CHECK (account_balance > 0)
);
```

## Primary and Foreign Keys

- PRIMARY KEY is equivalent to writing unique not null; Very common with ids  
   FOREIGN KEY has different syntax:
  `foreign_id REFERENCES other_table;`

- _FOREIGN KEYs created via REFERENCES must match a value in the ref table_
- _references will also look for ids by default: other-table(id) -> we can pass values in to override this_

---

## Deleting

Once we link tables with references we need to pay special attention to deletions;

---

## We'll be accounting for two behaviors primarily:

---

- Deleting data removes its references;
- Deleting data sets its corresponding references to NULL, or other value;

---

1. Cascading deletions: REFERENCE [column] ON DELETE CASCADE
   -This will delete all reference data  
   IE: a studio is deleted, and takes its movies with it;

---

2. SET NULL deletions - REFERENCE [column] ON DELETE SET NULL/DEFAULT
   -This will set reference data to null  
   IE: a reddit post with a NULL user;
3. ON DELETE RESTRICT / ON DELETE NO ACTION;

---

## Data Manipulation:

---

With the ALTER command we can change anything

```
ALTER TABLE books ADD COLUMN in_paperback BOOLEAN DEFAULT true;
ALTER TABLE books DROP COLUMN in_paperback;
ALTER TABLE books RENAME COLUMN page_count TO num_pages;
```

## **We will _NOT_ get deletion warnings when dropping columns!**
