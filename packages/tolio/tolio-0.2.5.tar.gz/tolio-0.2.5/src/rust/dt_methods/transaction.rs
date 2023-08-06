use std::collections::HashMap;
use std::error::Error;

use rusqlite::{named_params, Connection};

use crate::{
    data_types::{PreparedStatement, Transaction, UpdatedShare},
    db_methods::stock_split,
};

pub trait Get {
    fn get_institution_id(&self, db_path: &str) -> Result<i8, Box<dyn Error>>;

    fn get_security_id(&self) -> Result<i8, Box<dyn Error>>;
}

impl Transaction {
    pub fn get_recent_transaction(db_path: &str) -> Result<Transaction, Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "SELECT transaction_id, security_id, institution_id, timestamp, transaction_abbreviation,
        amount, price_USD, transfer_from, transfer_to, age_transaction, long FROM transactions WHERE transaction_id=(SELECT MAX(transaction_id) FROM transactions);";
        let mut prepared_sql = PreparedStatement::new(&conn, sql);
        let mut rows = prepared_sql.statement.query([])?;

        let mut vec: Vec<Transaction> = Vec::new();
        while let Some(row) = rows.next()? {
            let transaction_id: Option<i8> = row.get(0)?;
            let security_id: i8 = row.get(1)?;
            let institution_id: i8 = row.get(2)?;
            let timestamp: String = row.get(3)?;
            let transaction_abbreviation: String = row.get(4)?;
            let amount: f32 = row.get(5)?;
            let price_usd: Option<f32> = row.get(6)?;
            let transfer_from: Option<String> = row.get(7)?;
            let transfer_to: Option<String> = row.get(8)?;
            let age_transaction: i8 = row.get(9)?;
            let long: f32 = row.get(10)?;

            vec.push(Transaction {
                transaction_id: (transaction_id),
                security_id: (security_id),
                institution_id: (institution_id),
                timestamp: (timestamp),
                transaction_abbreviation: (transaction_abbreviation),
                amount: (amount),
                price_usd: (price_usd),
                transfer_from: (transfer_from),
                transfer_to: (transfer_to),
                age_transaction: (age_transaction),
                long: (long),
            })
        }
        Ok(vec[0].clone())
    }

    fn get_specific_all_shares(&self, db_path: &str) -> Result<Vec<UpdatedShare>, Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "SELECT individual_security_id, transaction_id, security_id, institution_id, timestamp, amount, price_USD, sold_price, age_transaction, long_counter, date_disposed FROM all_shares WHERE long_counter = '+' AND security_id=:security_id ORDER BY transaction_id;";
        let mut prepared_sql = PreparedStatement::new(&conn, sql);

        let share_iter = prepared_sql.statement.query_map(
            named_params! {":security_id": self.security_id},
            |row| {
                let individual_share_id = row.get(0)?;
                let transaction_id: i8 = row.get(1)?;
                let security_id: i8 = row.get(2)?;
                let institution_id: i8 = row.get(3)?;
                let timestamp: String = row.get(4)?;
                let amount: f32 = row.get(5)?;
                let price_usd: f32 = row.get(6)?;
                let sold_price: Option<f32> = row.get(7)?;
                let age_transaction: i8 = row.get(8)?;
                let long_counter: String = row.get(9)?;
                let date_disposed: Option<String> = row.get(10)?;

                Ok(UpdatedShare {
                    individual_share_id,
                    transaction_id,
                    security_id,
                    institution_id,
                    timestamp,
                    amount,
                    price_usd,
                    sold_price,
                    age_transaction,
                    long_counter,
                    date_disposed,
                })
            },
        )?;

        let mut security = Vec::new();
        for share in share_iter {
            security.push(share?);
        }
        Ok(security)
    }
    pub fn get_all_transactions(db_path: &str) -> Result<Vec<Transaction>, Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql = "SELECT * FROM transactions;";
        let mut prepared_sql = PreparedStatement::new(&conn, sql);
        let trans_iter = prepared_sql.statement.query_map([], |row| {
            let transaction_id: Option<i8> = row.get(0)?;
            let security_id: i8 = row.get(1)?;
            let institution_id: i8 = row.get(2)?;
            let timestamp: String = row.get(3)?;
            let transaction_abbreviation = row.get(4)?;
            let amount: f32 = row.get(5)?;
            let price_usd: Option<f32> = row.get(6)?;
            let transfer_from: Option<String> = row.get(7)?;
            let transfer_to: Option<String> = row.get(8)?;
            let age_transaction: i8 = row.get(9)?;
            let long = row.get(10)?;

            Ok(Transaction {
                transaction_id,
                security_id,
                institution_id,
                timestamp,
                transaction_abbreviation,
                amount,
                price_usd,
                transfer_from,
                transfer_to,
                age_transaction,
                long,
            })
        })?;
        let mut transactions: Vec<Transaction> = Vec::new();
        for transaction in trans_iter {
            transactions.push(transaction?);
        }
        dbg!(&transactions);
        Ok(transactions)
    }

    pub fn insert_into_all_shares(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;

        match self.transaction_abbreviation.clone().as_str() {
            "A" => {
                let amount = self.amount;
                let raw_price_usd = self.price_usd.unwrap();
                let whole_share = 1.0;
                if &amount > &whole_share {
                    let price_usd = &raw_price_usd / &amount;
                    let remainder = &amount % &whole_share;
                    let num_iter = &amount - &remainder;
                    for _ in 0..num_iter as i32 {
                        let sql = "INSERT INTO all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, long_counter, sold_price) VALUES (:transaction_id, :security_id, :institution_id, :timestamp, :amount, :price_USD, :age_transaction, :long_counter, :sold_price);";
                        let mut prepare_sql = PreparedStatement::new(&conn, sql);
                        prepare_sql.statement.execute(named_params! {
                            ":transaction_id": self.transaction_id,
                            ":security_id": self.security_id,
                            ":institution_id": self.institution_id,
                            ":timestamp": self.timestamp,
                            ":amount": &whole_share,
                            ":price_USD": &price_usd,
                            ":age_transaction": self.age_transaction,
                            ":long_counter": "+",
                            ":sold_price": 0.0
                        })?;

                        if &remainder > &0.0 {
                            let sql = "INSERT INTO all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, long_counter, sold_price) VALUES (:transaction_id, :security_id, :institution_id, :timestamp, :amount, :price_USD, :age_transaction, :long_counter, :sold_price);";
                            let mut prepare_sql = PreparedStatement::new(&conn, sql);
                            prepare_sql.statement.execute(named_params! {
                                ":transaction_id": self.transaction_id,
                                ":security_id": self.security_id,
                                ":institution_id": self.institution_id,
                                ":timestamp": self.timestamp,
                                ":amount": &remainder,
                                ":price_USD": &price_usd,
                                ":age_transaction": self.age_transaction,
                                ":long_counter": "+",
                                ":sold_price": 0.0
                            })?;
                        }
                    }
                } else if &amount <= &whole_share {
                    let price_usd = &raw_price_usd * &amount;
                    let sql = "INSERT INTO all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, long_counter, sold_price) VALUES (:transaction_id, :security_id, :institution_id, :timestamp, :amount, :price_USD, :age_transaction, :long_counter, :sold_price);";
                    let mut prepare_sql = PreparedStatement::new(&conn, sql);
                    prepare_sql.statement.execute(named_params! {
                        ":transaction_id": self.transaction_id,
                        ":security_id": self.security_id,
                        ":institution_id": self.institution_id,
                        ":timestamp": self.timestamp,
                        ":amount": &amount,
                        ":price_USD": &price_usd,
                        ":age_transaction": self.age_transaction,
                        ":long_counter": "+",
                        ":sold_price": 0.0


                    })?;
                }
            }

            "D" => {
                let shares = self.get_specific_all_shares(db_path)?;

                // Error if there are more shares to be disposed than shares available
                let total_available_shares = shares.len() as f32;

                if total_available_shares < self.amount.abs() {
                    panic!(
                        "ValueError: Total available shares of {available_shares} is less than
                    requested share disposal amount of {dispose_amount}",
                        available_shares = total_available_shares,
                        dispose_amount = self.amount
                    )
                } else {
                }

                let mut record: HashMap<&str, f32> = HashMap::new();
                record.insert("dispose", self.amount.abs());
                let dispose = "dispose";

                for share in shares.clone().into_iter() {
                    let mut share = share;

                    // Set the share.sold_price to zero if none to avoid mismatch type when performing arithmetic
                    match share.sold_price {
                        None => {
                            share.sold_price = Some(0.0);
                        }
                        _ => {}
                    }

                    let dispose_amount = record.get(&dispose).unwrap().clone();

                    if &share.amount > &dispose_amount {
                        let price_usd = self.price_usd.unwrap() * dispose_amount;
                        // share.sold_price is added to price_usd in case of previous share.sold_price value
                        share.sold_price = Some(share.sold_price.unwrap() + price_usd);
                        share.amount = share.amount - dispose_amount;
                        share.long_counter = String::from("-");
                        share.transaction_id = self.transaction_id.unwrap();
                        record.insert(&dispose, 0.0);

                        share.update_share(db_path)?;

                        // if the dipose amount reaches zero, break the loop
                        break;
                    } else if &share.amount < &dispose_amount {
                        let update_amount = record.get(&dispose).unwrap() - &share.amount;

                        if &dispose_amount > &1.0 {
                            let price_usd = self.price_usd.unwrap() / dispose_amount;
                            share.price_usd = price_usd;
                        } else {
                            let price_usd = self.price_usd.unwrap() * dispose_amount;
                            share.price_usd = price_usd;
                        }

                        share.amount = 0.0;
                        share.long_counter = String::from("-");
                        record.insert(&dispose, update_amount);

                        share.update_share(db_path)?;
                    } else if &share.amount == record.get(&dispose).unwrap() {
                        let price_usd = self.price_usd.unwrap() * dispose_amount;
                        // share.sold_price is added to price_usd in case of previous share.sold_price value
                        share.sold_price = Some(share.sold_price.unwrap() + price_usd);
                        share.amount = 0.0;
                        share.long_counter = String::from("-");
                        record.insert(&dispose, 0.0);
                        share.update_share(db_path)?;

                        break;
                    }
                }
            }

            "SS" => {
                self.split_all_shares(db_path).unwrap();
                let conn = Connection::open(db_path)?;
                let sql = "INSERT INTO stock_split_history (security_id, split_amount, timestamp) VALUES (:security_id,:split_amount,:timestamp);";
                let mut prepare_sql = PreparedStatement::new(&conn, sql);
                prepare_sql.statement.execute(named_params! {
                    ":security_id": self.security_id,
                    ":split_amount": self.amount,
                    ":timestamp": self.timestamp

                })?;
                stock_split::main(db_path).unwrap();
            }

            "T" => {
                let conn = Connection::open(db_path)?;
                for _ in 0..self.amount as i32 {
                    let sql = "UPDATE all_shares SET transaction_id = :transaction_id, institution_id = :transfer_to_institution_id
                WHERE security_id = :security_id AND institution_id = :institution_id AND
                individual_share_id = (
                SELECT min(individual_share_id)
                FROM All_shares
                WHERE long_counter = '+' AND institution_id = :institution_id AND amount = 1);";
                    let mut prepare_sql = PreparedStatement::new(&conn, sql);
                    prepare_sql.statement.execute(named_params! {
                        ":transaction_id": self.transaction_id,
                        ":transfer_to_institution": self.transfer_to,
                        ":security_id": self.security_id,
                        ":institution_id": self.institution_id,

                    })?;
                }
            }

            _ => {}
        }

        Ok(())
    }
    // method to multiply the existing shares of interest within all_shares for the stock_split method
    pub fn split_all_shares(&self, db_path: &str) -> Result<(), Box<dyn Error>> {
        let conn = Connection::open(db_path)?;
        let sql =
            "UPDATE all_shares SET amount=:amount WHERE long_counter='+' AND security_id = :security_id
        AND (timestamp IS NULL OR timestamp > :timestamp);";
        let mut prepare_sql = PreparedStatement::new(&conn, sql);
        prepare_sql.statement.execute(named_params! {":amount":self.amount, ":security_id": self.security_id, ":timestamp":self.timestamp})?;

        Ok(())
    }
}
