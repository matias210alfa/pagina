import { formatCurrency } from '../utils/format';

export default function BalanceCard({ balance }) {
  const isPositive = balance >= 0;

  return (
    <div style={styles.card}>
      <p style={styles.label}>Saldo Actual</p>
      <h1 style={{
        ...styles.amount,
        color: isPositive ? 'var(--accent-green)' : 'var(--accent-red)',
      }}>
        {formatCurrency(balance)}
      </h1>
      <div style={styles.indicator}>
        <div style={{
          ...styles.dot,
          backgroundColor: isPositive ? 'var(--accent-green)' : 'var(--accent-red)',
        }} />
        <span style={styles.status}>
          {isPositive ? 'Balance positivo' : 'Balance negativo'}
        </span>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: 'linear-gradient(135deg, var(--bg-card) 0%, #1a2744 100%)',
    borderRadius: 'var(--radius)',
    padding: '28px 24px',
    textAlign: 'center',
    border: '1px solid var(--border)',
    boxShadow: 'var(--shadow)',
    marginBottom: '20px',
  },
  label: {
    color: 'var(--text-secondary)',
    fontSize: '14px',
    fontWeight: 500,
    marginBottom: '8px',
    textTransform: 'uppercase',
    letterSpacing: '1.5px',
  },
  amount: {
    fontSize: '42px',
    fontWeight: 800,
    margin: '4px 0 12px',
    letterSpacing: '-1px',
  },
  indicator: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  },
  dot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
  },
  status: {
    color: 'var(--text-muted)',
    fontSize: '13px',
    fontWeight: 500,
  },
};
