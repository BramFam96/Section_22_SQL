# Modeling Data

## Visualizing DB Structure

_We should visualize DB structure with some form of diagram prior to making them_

- Color coded excel
- Crow's Foot Notation

  - [Quick Database Diagram](app.quickdatabasediagrams.com/#/)

QuickDBD lets us create tables with text, and link relationships visually

---

## Normalization

**Normalization** is a design technique aimed at **reducing** data _redundancy_ and _dependency_  
The process involves dividing larger tables into smaller tables and links  
&nbsp;  
**it has a very high skill ceiling** - googling will result in crazy jargon!  
Our signal to split tables is _duplicate entries_

---

## Non-normalized example:

```
SALES TEAM
id  name   office  office_phone  customer1 customer2 customer3
1   Chuck  San F   (415)...      Fender    Gibson
2   Ella   NY      (212)...      Gibson    Martin    Fender
3   James  San F   (415)...      Martin    Fender
```

## **Duplication is rampant!**

1. Sales people and office have a 1:M relationship:
2. Sales and cust have M:M relationship

**We would make the tables:**

- Sales
- Office
- Customer
- Sales_customer

_We could also reduce the number of cust sales can take on (one or two) and avoid Sales_Customer table_

## Indexing

A **DB index** speeds up _read queries_ (row retrievel) by more efficienctly storing _column values_  
Indexes work like a _table of contents_ allowing us to mark and skip to relevant sections of our DB  
&nbsp;  
Example  
We could place an **index** on _username_, and speed up any queries using _username_  
&nbsp;  
**Technical Jargon**: Indexs retrieve values in **O(lg(N))** time - _remember log graphs platue into constant time_

- **O(n)** is linear time - 1,000,000 rows will require 1,000,000 cells scanned
- **O(lg(N))** at even an N of 2 reduces 1,000,000 down to 20  
  &nbsp;  
  We'll discuss _Big O Notation_ in future lessons

## Why not index everything?

Indexes have tradeoffs to consider!

- Duplication
  - **Every** indexed column is copied and stored as a b tree
  - This **doubles** _memory_, and _INSERT/UPDATE operations_

Only index values that you know you'll use:  
Users will be selected via _name_, **not** _password, address, or sign-up date_

---

## Making Indexes

Indexes can be **added** or **dropped** _anytime_ with DDL  
Indexing is a process with a **direct relationship** b/w _data size_ and _time_

- _More records will slow the process down_

```
CREATE INDEX index_name ON table_name (column_name)
```

We can also create a multi-column index if we're constantly querying by two fields at once:  
_first-name, last-name_

```
CREATE INDEX index_name ON table_name (column1_name, column2_name)
```

_NOTE_ when we specify data as **UNIQUE** in DDL psql also creates an **index**
