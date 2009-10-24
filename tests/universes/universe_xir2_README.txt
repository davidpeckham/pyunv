Universe Sample_A

Description: This is the first sample universe for PyUnv tests. It uses the pyunv_a database.

Comments: These are comments for the Sample_A universe.

Created 9/23/2009 by peckhda

This universe was not saved for all users


Strategies

Objects: (Built-in) Standard Renaming
Joins: Edit Manually (none)
Tables: (Built-in) Standard

Controls

Limit size of results to: 54321 rows
Limit execution time to: 37 minutes
Warn if cost estimate exceeds: 5 minutes (this option is disabled)
Limit size of long text objects to: 1234 characters

SQL

Query
Allow use of subqueries (enabled)
Allow use of union, intersect and minus operations (enabled)
Allow complex operands in Query Panel (enabled)

Multiple Paths
Multiple SQL statements for each context (enabled)
Multiple SQL statements for each measure (enabled)
Allow selection of multiple contexts (disabled)

Cartesian Products
Warn (not Prevent)

Parameters

SAMPLE_PARAMETER is set to 999333
SAMPLE_PARAMETER2 is set to 999222

Connection Information

Connection Name: pyunv_a_connection
Connection Type: Personal
Database Engine: Generic ODBC3 datasource
Data source name: pyunv_a_odbc
Network layer: ODBC
Language: en
Charset: CP1252
BusinessObjects Version: 11.5..313.313


Advanced Parameters

Keep the connection alive for 26 minutes
Array fetch size: 17
Array bind size: 18
Login timeout: 619


Custom ODBC parameters

Binary Slice Size: 1029


Contexts

CustomerOrder ("This is the CustomerOrder context.") includes orderline, orderinfo, and customer
ItemStock ("This is the ItemStock context.") includes barcode, stock, and item

Derived Tables

CheapItems = select * from public.item where sell_price <= 1000
ExpensiveItems = select 8 from public.item where sell_price > 1000

Alias

SalesOrders is an alias for public.orderinfo

Custom Hierarchy

Customer / OrderInfo / OrderLine / Item

