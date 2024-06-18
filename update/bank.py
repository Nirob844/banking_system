class BankAccount:
    account_counter = 1000
    
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0
        
    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount}")
        print(f"Deposited {amount} successfully.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew {amount}")
            print(f"Withdrew {amount} successfully.")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history
    
    def take_loan(self, amount):
        if Bank.loan_feature_enabled:
            if self.loan_count < 2:
                self.balance += amount
                self.loan_count += 1
                self.transaction_history.append(f"Took loan of {amount}")
                Bank.total_loan_amount_value += amount
                print(f"Loan of {amount} approved.")
            else:
                print("Loan limit reached. Cannot take more than two loans.")
        else:
            print("Loan feature is currently disabled.")

    def transfer(self, amount, other_account):
        if self.balance < amount:
            print("Insufficient balance")
        elif isinstance(other_account, BankAccount):
            if amount > self.balance:
                print("Insufficient funds for transfer")
            else:
                self.balance -= amount
                other_account.balance += amount
                self.transaction_history.append(f"Transferred {amount} to account {other_account.account_number}")
                other_account.transaction_history.append(f"Received {amount} from account {self.account_number}")
                print(f"Transferred {amount} to account {other_account.account_number} successfully.")
        else:
            print("Account does not exist")


class Bank:
    accounts = []
    total_loan_amount_value = 0
    loan_feature_enabled = True
    
    @classmethod
    def create_account(cls, name, email, address, account_type):
        account = BankAccount(name, email, address, account_type)
        cls.accounts.append(account)
        print(f"Account created successfully for {name} with account number {account.account_number}")
        return account

    @classmethod
    def delete_account(cls, account_number):
        account = cls.find_account(account_number)
        if account:
            cls.accounts.remove(account)
            print(f"Account number {account_number} deleted successfully.")
        else:
            print("Account does not exist")

    @classmethod
    def list_accounts(cls):
        for account in cls.accounts:
            print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")
    
    @classmethod
    def total_available_balance(cls):
        total_balance = sum(account.balance for account in cls.accounts)
        return total_balance
    
    @classmethod
    def total_loan_amount(cls):
        return cls.total_loan_amount_value
    
    @classmethod
    def enable_loan_feature(cls, enable=True):
        cls.loan_feature_enabled = enable
        status = "enabled" if enable else "disabled"
        print(f"Loan feature has been {status}.")

    @staticmethod
    def find_account(account_number):
        for account in Bank.accounts:
            if account.account_number == account_number:
                return account
        return None

# Example Usage
bank = Bank()

# Admin functionalities
user1 = bank.create_account("John Doe", "john@example.com", "123 Elm Street", "Savings")
user2 = bank.create_account("Jane Smith", "jane@example.com", "456 Oak Avenue", "Current")

# User functionalities
user1.deposit(1000)
user1.withdraw(500)
print(user1.check_balance())
print(user1.check_transaction_history())
user1.take_loan(2000)
user1.transfer(1000, user2)
print(user2.check_balance())
print(user2.check_transaction_history())

user1.withdraw(3000)  # Trying to withdraw more than the balance to trigger the error

bank.list_accounts()
print(f"Total available balance in the bank: {bank.total_available_balance()}")
print(f"Total loan amount in the bank: {bank.total_loan_amount()}")

bank.delete_account(user1.account_number)
bank.list_accounts()

bank.enable_loan_feature(False)
user2.take_loan(1000)
bank.enable_loan_feature(True)
user2.take_loan(1000)
