// Replace this URL with your actual API Gateway Invoke URL
const apiUrl = 'https://<api_id>.execute-api.us-east-1.amazonaws.com/dev';

// Function to handle user sign-up
async function signUp() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;

    const response = await fetch(`${apiUrl}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailId: email, firstName, lastName })
    });

    const data = await response.json();
    alert(data.message);
}

// Function to handle user login
async function login() {
    const email = document.getElementById('loginEmail').value;

    const response = await fetch(`${apiUrl}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailId: email })
    });

    const data = await response.json();
    if (response.status === 200) {
        alert('Login successful');
        document.getElementById('expense-form').style.display = 'block';
        document.getElementById('expense-list').style.display = 'block';
        document.getElementById('login').style.display = 'none';
        document.getElementById('sign-up').style.display = 'none';
    } else {
        alert(data.message);
    }
}

// Function to add a new expense
async function addExpense() {
    const email = document.getElementById('loginEmail').value;
    const date = document.getElementById('date').value;
    const description = document.getElementById('description').value;
    const amount = parseFloat(document.getElementById('amount').value);

    const response = await fetch(`${apiUrl}/add-expense`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailId: email, date, description, amount })
    });

    const data = await response.json();
    alert(data.message);
    if (response.status === 200) {
        fetchExpenses(email);
    }
}

// Function to fetch and display expenses
async function fetchExpenses(email) {
    try {
        const response = await fetch(`${apiUrl}/get-expenses?emailId=${email}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        const expensesList = document.getElementById('expenses');
        expensesList.innerHTML = '';

        // Check if the response contains the 'expenses' array
        if (response.ok && data.expenses && Array.isArray(data.expenses)) {
            if (data.expenses.length === 0) {
                expensesList.innerHTML = '<li>No expenses found</li>';
            } else {
                data.expenses.forEach(expense => {
                    const li = document.createElement('li');
                    li.textContent = `Date: ${expense.date}, Description: ${expense.description}, Amount: $${expense.amount}`;
                    expensesList.appendChild(li);
                });
            }
        } else {
            console.error('Unexpected response format:', data);
            alert('Failed to load expenses. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching expenses:', error);
        alert('Error: Unable to fetch expenses from server.');
    }
}



// Function to handle user logout
function logout() {
    document.getElementById('expense-form').style.display = 'none';
    document.getElementById('expense-list').style.display = 'none';
    document.getElementById('login').style.display = 'block';
    document.getElementById('sign-up').style.display = 'block';
    alert('Logged out');
}
