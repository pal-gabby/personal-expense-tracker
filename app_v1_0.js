import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://5b5ryu7o07.execute-api.us-east-1.amazonaws.com/dev/expenses';

function App() {
  const [expenses, setExpenses] = useState([]);
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const user_id = '2418b4e8-d051-7082-18ca-f7db0ee4a84d'; // Replace with the actual user ID from Cognito

  // Fetch expenses
  const fetchExpenses = async () => {
    try {
      const response = await fetch(API_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Failed to fetch expenses");
      }
      const data = await response.json();
      setExpenses(data);
    } catch (error) {
      console.error("Error fetching expenses:", error);
    }
  };

  // Add an expense
  const addExpense = async () => {
    const newExpense = {
      amount,
      category,
      description,
      user_id,
    };

    try {
      // Using Axios with the correct API URL
      await axios.post(API_URL, newExpense, {
        headers: { 'user_id': user_id },
      });
      alert('Expense added successfully!');
      setAmount('');
      setCategory('');
      setDescription('');
      fetchExpenses(); // Refresh the expense list
    } catch (error) {
      console.error('Error adding expense:', error);
      alert('Failed to add expense.');
    }
  };

  // Load expenses when the component mounts
  useEffect(() => {
    fetchExpenses();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Personal Expense Tracker</h1>
      <div>
        <input
          type="text"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <input
          type="text"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button onClick={addExpense}>Add Expense</button>
      </div>
      <h2>Expense List</h2>
      <ul>
        {expenses.map((expense, index) => (
          <li key={index}>
            {expense.timestamp} - {expense.category}: ${expense.amount} ({expense.description})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
