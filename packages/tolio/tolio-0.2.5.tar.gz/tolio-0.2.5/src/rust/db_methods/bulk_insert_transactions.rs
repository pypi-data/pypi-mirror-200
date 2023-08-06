use rusqlite::{Connection, Result, ToSql, Transaction};
use std::error::Error;

use crate::data_types::EditedRawTransaction;

pub fn batch_insert(
    count: usize,
    tx: &Transaction,
    vector_proto: Vec<EditedRawTransaction>,
) -> Result<(), Box<dyn Error>> {
    let mut vector = vector_proto.clone();
    // Determine the batch size
    let mut min_batch_size = 50;
    let mut remainder: bool = false;
    let mut remainder_amount = 0;
    let mut times_iter = 1;

    if count <= min_batch_size {
        min_batch_size = count;
    } else if count > min_batch_size {
        remainder = true;
        // Must convert usize to integer for floor division
        let count = count as i32;
        let min_batch_size = min_batch_size as i32;

        // integer divided by integer will give floor division
        times_iter = count / min_batch_size;

        // change main scope remainder_amount
        remainder_amount = count - (times_iter * min_batch_size);
    }
    // Create the parameters of insert for the sql query
    let mut insert_param = " (?,?,?,?,?,?,?,?,?,?),".repeat(min_batch_size as usize);
    // Because the original counts, the total would be 51, but pop will bring it down to 50
    insert_param.pop();
    let insert_param = insert_param.as_str();

    // Create the standardized query
    let st = format!("INSERT INTO transactions(security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long)
    VALUES {};", insert_param);

    let mut sql_statement = tx.prepare_cached(st.as_str()).unwrap();
    for _ in 0..(times_iter) {
        let mut param_values: Vec<_> = Vec::new();
        let push_vec: Vec<_> = vector.drain(..&min_batch_size).collect();
        for batch in push_vec.iter() {
            param_values.push(&batch.security_id as &dyn ToSql);
            param_values.push(&batch.institution_id as &dyn ToSql);
            param_values.push(&batch.timestamp as &dyn ToSql);
            param_values.push(&batch.transaction_abbreviation as &dyn ToSql);
            param_values.push(&batch.amount as &dyn ToSql);
            param_values.push(&batch.price_usd as &dyn ToSql);
            param_values.push(&batch.transfer_from as &dyn ToSql);
            param_values.push(&batch.transfer_to as &dyn ToSql);
            param_values.push(&batch.age_transaction as &dyn ToSql);
            param_values.push(&batch.long as &dyn ToSql);
        }
        sql_statement.execute(&*param_values).unwrap();
    }
    // add the remainder that was not part of the complete 50
    if remainder == true {
        let mut insert_param = " (?,?,?,?,?,?,?,?,?,?),".repeat(remainder_amount as usize);
        insert_param.pop();
        let insert_param = insert_param.as_str();

        // Create the standardized query
        let st = format!("INSERT INTO transactions(security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long)
        VALUES {};", insert_param);
        let mut sql_statement = tx.prepare_cached(st.as_str()).unwrap();

        let mut param_values: Vec<_> = Vec::new();
        let push_vec: Vec<_> = vector.drain(0..).collect();
        for batch in push_vec.iter() {
            param_values.push(&batch.security_id as &dyn ToSql);
            param_values.push(&batch.institution_id as &dyn ToSql);
            param_values.push(&batch.timestamp as &dyn ToSql);
            param_values.push(&batch.transaction_abbreviation as &dyn ToSql);
            param_values.push(&batch.amount as &dyn ToSql);
            param_values.push(&batch.price_usd as &dyn ToSql);
            param_values.push(&batch.transfer_from as &dyn ToSql);
            param_values.push(&batch.transfer_to as &dyn ToSql);
            param_values.push(&batch.age_transaction as &dyn ToSql);
            param_values.push(&batch.long as &dyn ToSql);
        }
        sql_statement.execute(&*param_values).unwrap();
    }
    Ok(())
}

pub fn insert(tx: &Transaction, vector: Vec<EditedRawTransaction>) {
    let count = vector.len() as usize;

    batch_insert(count, tx, vector).expect("Error: batch insert error.");
}

pub fn insert_wrapper(conn: &mut Connection, vector: Vec<EditedRawTransaction>) {
    let tx = conn.transaction().unwrap();

    insert(&tx, vector);
    tx.commit().unwrap();
}

pub fn main(path: String, vec_transactions: Vec<EditedRawTransaction>) -> Result<()> {
    let path_ = path.clone();
    let conn = &mut Connection::open(path_).unwrap();

    insert_wrapper(conn, vec_transactions);

    let tx = conn.transaction()?;
    tx.commit()
}
