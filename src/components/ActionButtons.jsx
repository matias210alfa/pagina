export default function ActionButtons({ onAdd }) {
  return (
    <div style={styles.container}>
      <button
        style={{ ...styles.button, ...styles.incomeBtn }}
        onClick={() => onAdd('ingreso')}
      >
        <span style={styles.icon}>+</span>
        <span>Ingreso</span>
      </button>
      <button
        style={{ ...styles.button, ...styles.expenseBtn }}
        onClick={() => onAdd('egreso')}
      >
        <span style={styles.icon}>−</span>
        <span>Egreso</span>
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '12px',
    marginBottom: '24px',
  },
  button: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    padding: '16px',
    borderRadius: 'var(--radius-sm)',
    fontSize: '16px',
    fontWeight: 600,
    border: 'none',
  },
  incomeBtn: {
    background: 'var(--accent-green-bg)',
    color: 'var(--accent-green)',
    border: '1px solid rgba(0, 214, 143, 0.2)',
  },
  expenseBtn: {
    background: 'var(--accent-red-bg)',
    color: 'var(--accent-red)',
    border: '1px solid rgba(255, 107, 107, 0.2)',
  },
  icon: {
    fontSize: '22px',
    fontWeight: 700,
    lineHeight: 1,
  },
};
