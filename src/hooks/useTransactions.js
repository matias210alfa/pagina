import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'caja-chica-transactions';

function loadTransactions() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

function saveTransactions(transactions) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(transactions));
}

export function useTransactions() {
  const [transactions, setTransactions] = useState(loadTransactions);

  useEffect(() => {
    saveTransactions(transactions);
  }, [transactions]);

  const balance = transactions.reduce((acc, t) => {
    return t.type === 'ingreso' ? acc + t.amount : acc - t.amount;
  }, 0);

  const addTransaction = useCallback((type, amount, concept) => {
    const newTransaction = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      type,
      amount: parseFloat(amount),
      concept,
    };
    setTransactions(prev => [newTransaction, ...prev]);
  }, []);

  const deleteTransaction = useCallback((id) => {
    setTransactions(prev => prev.filter(t => t.id !== id));
  }, []);

  return { transactions, balance, addTransaction, deleteTransaction };
}
