'''database.py - interaction with database methods that includes tolio rust extension'''
import sqlite3
import os

from typing import List, Any

import tolio

class Database:
    '''Class that contains all database methods'''
    def __init__(self, db_path: str="files/data/portfolio.db", sql_path: str="src/database/init_db.sql") -> None:
        '''initialize with preset paths to db and sql'''
        # locate database
        self.db_path = os.path.expanduser(db_path)

        # create a new data directory if there is not one previously
        # this solves the error of not being able to create a new db because the directory did not exist
        data_dir = "files/data"
        if not os.path.exists(data_dir):
          os.makedirs(data_dir)
          self.connection = sqlite3.connect(os.path.expanduser(data_dir + "/portfolio.db"))
        self.connection = sqlite3.connect(os.path.expanduser(self.db_path))
        self.cur = self.connection.cursor()

    # ============================== create tables ==============================

        self.execute_sql_script(os.path.expanduser(sql_path))
        self.connection.commit()

    # create .sql file to create the tables
    def execute_sql_script(self, filename):
        '''method to execute sql'''
        file_open = open(filename, 'r')
        sql_file = file_open.read()
        file_open.close()
        sql_commands = sql_file.split(";")
        for command in sql_commands:
            try:
                self.cur.execute(command)
            except sqlite3.OperationalError as msg:
                print("Command skipped: ", msg)

  # ============================== insert ==============================

    #All of the following insert methods affects the all_shares table

    # insert a acquire or dispose (add) transaction into transactions
    def insert_acquire_or_dispose(self, value_dic: dict[Any]) -> None:
        '''method to insert an acquire or dipose transaction'''
        tolio.insert_acquire_or_dispose(self.db_path, value_dic)

    # insert a transfer transaction into transactions
    def insert_transfer(self, value_dic: dict[Any]) -> None:
        '''method to insert a transfer transaction'''
        tolio.insert_transfer(self.db_path, value_dic)

  # insert a stock split transaction into transaction
    def insert_stock_split(self, value_dic: dict[Any]) -> None:
        '''method to insert a stock split transaction'''
        tolio.insert_stock_split(self.db_path, value_dic)

  # ============================== update tables ================================

  # update transaction age
    def update_transaction_age(self) -> None:
        '''method to update transaction age'''
        tolio.update_transaction_age(self.db_path)

  # update securities - this dependent on the all_shares table
    def update_securities(self) -> None:
        '''method to update securities table'''
        # create list of securities
        sql = "SELECT DISTINCT security_id FROM transactions WHERE transaction_abbreviation IS NOT 'SS';"
        get_securities=self.cur.execute(sql).fetchall()
        for security_id in get_securities:
            security_id = security_id[0]

            sql = "SELECT SUM(amount) FROM all_shares WHERE security_id=? AND age_transaction >= 1 AND long_counter = '+';"
            age = self.cur.execute(sql, (security_id,)).fetchall()[0]

            self.cur.execute("UPDATE securities SET number_long=? WHERE security_id=?;", (age[0], security_id))

            sql = "SELECT SUM(amount), SUM(price_USD), (SUM(price_USD)/SUM(amount)), (SELECT SUM(amount) FROM transactions WHERE transaction_abbreviation='D') FROM all_shares WHERE security_id=? AND long_counter = '+';"
            amount=self.cur.execute(sql, (security_id,)).fetchall()[0]

            (sum_amount, sum_price, cost_basis, amount_disposed) = amount

            get_data_2 = self.cur.execute("""SELECT (SELECT SUM(amount) FROM all_shares WHERE long_counter='+' AND age_transaction > 0 AND security_id=?), SUM(sold_price) FROM all_shares WHERE security_id=?;""", (security_id, security_id)).fetchall()[0]

            (_, total_price_sold) = get_data_2

            if amount_disposed == None or amount_disposed == 0 or total_price_sold == None:
                average_price_sold = 0
            else:
                average_price_sold = round(float(total_price_sold) / abs(amount_disposed),3)

            try:
                total_price_sold = round(total_price_sold, 2)
            except:
                total_price_sold = 0

            sql = "UPDATE securities SET amount_held=?, total_cost=?, cost_basis=?, total_price_sold=?, average_price_sold=? WHERE security_id=?;"
            self.cur.execute(sql,
                             (sum_amount,
                              round(sum_price, 3),
                              round(cost_basis, 3),
                              total_price_sold,
                              average_price_sold,
                              security_id))

        self.connection.commit()

    # update institutions held: institution_id, security_id, amount_held, total_cost, cost_basis, number_long
    def update_institutions_held(self) -> None:
        '''method to update institutions held table'''
        get_institution_id = self.cur.execute("SELECT DISTINCT institution_id, security_id FROM Transactions").fetchall()
        for institution_id, security_id in get_institution_id:

            self.cur.execute("INSERT OR IGNORE INTO institutions_held (institution_id, security_id) VALUES (?,?);", (institution_id, security_id))
            get_data=self.cur.execute("""SELECT SUM(amount), SUM(price_USD), (SUM(price_USD)/(SUM(amount))), (SELECT SUM(amount) FROM transactions WHERE transaction_abbreviation='D')
            FROM All_shares WHERE institution_id=? AND security_id=? AND long_counter ='+';""", (institution_id, security_id)).fetchall()[0]

            (amount_held, total_cost, cost_basis, amount_disposed)=get_data
            if bool(total_cost) == False:
              total_cost = 0
            if bool(cost_basis) == False:
              cost_basis = 0
            if bool(amount_disposed) == False:
              amount_disposed = 0

            place_holder = {
              "security_id": security_id,
              "institution_id": institution_id,
              "amount_held": amount_held,
              "total_cost": round(total_cost,3),
              "cost_basis": round(cost_basis,3),
              "amount_disposed": round(amount_disposed,3)
            }

            get_data_2 = self.cur.execute("SELECT (SELECT SUM(amount) FROM all_shares WHERE long_counter='+' AND age_transaction > 0 AND institution_id = :institution_id AND security_id = :security_id), SUM(sold_price), (SELECT SUM(amount) FROM all_shares WHERE long_counter = '-' AND institution_id = :institution_id AND security_id=:security_id) FROM all_shares WHERE institution_id = :institution_id AND security_id=:security_id;", place_holder).fetchall()
            (long, total_price_sold, total_amount_sold) = get_data_2[0]

            place_holder["long"] = long

            if bool(total_price_sold) == False:
              total_price_sold = 0
            if bool(total_amount_sold) == False:
              average_price_sold = 0
            elif bool(total_amount_sold) == True:
              average_price_sold = round(total_price_sold/total_amount_sold, 3)
            place_holder["total_price_sold"] = total_price_sold
            place_holder["average_price_sold"] = average_price_sold
            self.cur.execute("UPDATE institutions_held SET amount_held=:amount_held, total_cost=:total_cost, cost_basis=:cost_basis, number_long=:long, total_price_sold=:total_price_sold, average_price_sold=:average_price_sold WHERE institution_id=:institution_id AND security_id=:security_id;", place_holder)
        self.connection.commit()


    # update table from transactions table
    def update_table(self, value_dic: dict[Any]) -> None:
        '''method to update transaction table'''
        tolio.update_table(self.db_path, value_dic)

    # ================================= get =================================

    # get stock_split_history for tree view
    def get_stock_split_history(self) -> List[Any]:
        '''method to return stock_split_history'''
        split_history_list = self.cur.execute("""SELECT ss.security_id, s.security_name, s.security_ticker, ss.split_amount, ss.timestamp FROM stock_split_history AS ss
        INNER JOIN securities AS s ON ss.security_id=s.security_id;""").fetchall()
        return split_history_list

    # get transactions table for tree view
    def get_transactions_table(self) -> List[str]:
        '''method to return all of the transactions in database'''
        return self.cur.execute("""SELECT
          t.transaction_id, s.security_name, s.security_ticker, i.institution_name, t.timestamp,
          tn.transaction_type, t.transfer_from, t.transfer_to, t.price_USD, t.amount,
          t.age_transaction, t.long
          FROM institutions as i INNER JOIN transactions AS t ON i.institution_id=t.institution_id
          INNER JOIN transaction_names AS tn ON t.transaction_abbreviation=tn.transaction_abbreviation
          INNER JOIN securities AS s USING(security_id)""").fetchall()

    # get institutions_held table for treeview
    def get_institutions_held_table(self) -> List[str]:
        '''method to return all of the values in the institutions held table'''
        return self.cur.execute("""
          SELECT i.institution_name, s.security_name, ih.amount_held, ih.total_cost, ih.cost_basis,
          ih.number_long, ih.total_price_sold, ih.average_price_sold
          FROM securities as s INNER JOIN institutions_held AS ih ON s.security_id=ih.security_id
          INNER JOIN institutions AS i USING(institution_id)
          """).fetchall()

    # get the securities table for treeview
    def get_security_table(self) -> List[str]:
        '''method to return all of the values in the securities table'''
        return self.cur.execute("""
          SELECT security_name, security_ticker, amount_held, total_cost, cost_basis, number_long, total_price_sold, average_price_sold
          FROM securities;
          """).fetchall()

    # get list of x that exists
    def get_table_value(self,value:str) -> List[str]:
        '''method to get a list of preexisting values to help auto-complete input in entry box'''
        edited_array = []
        if value == "security_name":
          unedited_list = self.cur.execute("SELECT DISTINCT security_name FROM securities;").fetchall()
        elif value == "security_ticker":
          unedited_list = self.cur.execute("SELECT DISTINCT security_ticker FROM securities;").fetchall()
        elif value == "institution":
          unedited_list = self.cur.execute("SELECT DISTINCT institution_name FROM institutions;").fetchall()
        else:
          unedited_list = []
        if len(unedited_list) == 0:
          return [""]
        elif len(unedited_list) > 0:
          for i in unedited_list:
            edited_array.append(i[0])
          return edited_array

    # ============================== delete ==============================
    # delete transaction row
    def delete_row(self, transaction_id:int) -> None:
        '''method to delete row in the database form gui treeview deletion'''
        self.cur.execute("DELETE FROM transactions WHERE transaction_id=?;", (transaction_id,))
        self.connection.commit()

    # delete all transactions records
    def delete_all_data(self) -> None:
        '''method to delete all of the values from transactions table'''
        self.cur.execute("DELETE TABLE transactions;")
        self.connection.commit()

# test
if __name__ =="__main__":
    data = Database()