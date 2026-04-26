import { useState } from 'react';
import { useTransactions } from './hooks/useTransactions';
import BalanceCard from './components/BalanceCard';
import ActionButtons from './components/ActionButtons';
import TransactionList from './components/TransactionList';
import TransactionForm from './components/TransactionForm';

export default function App() {
  const { transactions, balance, addTransaction, deleteTransaction } = useTransactions();
  const [formType, setFormType] = useState(null);

  const handleSave = (type, amount, concept) => {
    addTransaction(type, amount, concept);
    setFormType(null);
  };

  return (
    <div className="app-container">
      <header style={styles.header}>
        <h1 style={styles.title}>Caja Chica</h1>
      </header>

      <BalanceCard balance={balance} />
      <ActionButtons onAdd={setFormType} />
      <TransactionList
        transactions={transactions}
        onDelete={deleteTransaction}
      />

      {formType && (
        <TransactionForm
          type={formType}
          onSave={handleSave}
          onCancel={() => setFormType(null)}
        />
      )}
    </div>
  );
}

const styles = {
  header: {
    padding: '20px 0 16px',
    textAlign: 'center',
  },
  title: {
    fontSize: '22px',
    fontWeight: 700,
    color: 'var(--text-primary)',
    letterSpacing: '-0.5px',
  },
};
