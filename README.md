virtual environment is NOT submitted. Please install it by yourself. 
To install virtual environment, go to the bottom right of the screen, it will say no interpreter. Click on that and 
add new interpreter.

1. Once VENV is installed, go to requirements.txt. install ALL packages.
2. Go to models/cust/nltk_utils.py and uncomment the # nltk.download('punkt'). This will allow you to download 'punkt' 
so that the chatbot can function
3. Now, you are ready to go.
4. Currently, there are admin accounts already made. test1, test2 all the way to test10. No customer accounts are made,
and you are unable to login as a customer. PLEASE create a customer by registering. 
5. After registering, you can log in as a customer. If you need more admin accounts to check out our pagination function,
go to main.py and all the way below, before the function below, type massAccount(number of accounts you want to add)
if __name__ == '__main__':
    app.run(debug=True)
6. email username and password is in config.py please do not hack into my account. I wanted to use my operating system, 
but you wouldn't have authorisation, so I'll just put it there.

Changes made
Account management = Forget Password function. (Will send you email url to a page with a token that includes your 
user_id in the token, along with the secret_key and algorithm using jwt.)

Bugs fixed for:
adding products
adding resumes
adding job positions
