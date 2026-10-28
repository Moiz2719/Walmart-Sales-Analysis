# Local source data

Place your authorised SQLite database in this folder as:

`customer_churn.db`

The notebook PDF references a database at `/content/customer_churn.db` and reads three tables:

- `db_customer`
- `db_subscription`
- `db_support`

The database file was not attached with the PDF, so it must be supplied separately to run the code. The scripts stop with a helpful error if the file or expected tables are missing.

**Keep customer data private.** The example schema contains names, dates of birth, customer IDs, and support comments. The Git ignore rules exclude database and CSV files. Do not override those rules to publish identifiable customer data.
