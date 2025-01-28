import os
import sqlite3

class DataBaseManager:
    def __init__(self, database= "expenses.db") -> None:
        
        '''
        General initialization
        Initializes the database name
        '''
        self.dbName : str = database
        
    def initializeDatabase(self) -> None:
        
        """
        create a databse called dbName default = expenses
        if database exists passes
        """
        
        if os.path.exists(self.dbName):
            raise Exception("Database exists")
        else:
            with self._connect(self.dbName) as conn:
                c = conn.cursor()
                c.execute("""CREATE TABLE expenses (
                    DATE text,
                    EXPENSENAME text,
                    AMOUNT real,
                    TYPE text,
                    CURRENCY text
                    )""")
                
    def _connect(self, name : str) -> sqlite3.Connection:
        """
        Returns connection. Private function not to be referenced outside
        """
        return sqlite3.connect(name)
    
    def addExpense(self, query : str) -> None:
        """
        Adding to the database based on query provided
        """
        
        with self._connect(self.dbName) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
       
            
    def deleteExpense(self, query : str) -> None:
        """
        Deletes from database 
        Args:
            query (str): sqlite statement
        """
        
        with self._connect(self.dbName) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            
    def getExpense(self, query : str) -> list[tuple,str,float]:
        """
        Get expenses as tuple
        
        Args:
            query (str): sqlite string

        Returns:
            dict[str,float]: returns all as a list of tuples
        """
        
        with self._connect(self.dbName) as conn:
            c = conn.cursor()
            c.execute(query)
            
            return c.fetchall()
        
    def getTotalYears(self, query : str) -> NotImplementedError:
        raise NotImplementedError()