import { formatCurrency, formatDate } from '../utils/format';

export default function TransactionList({ transactions, onDelete }) {
  if (transactions.length === 0) {
    return (
      <div style={styles.empty}>
        <p style={styles.emptyIcon}>📋</p>
        <p style={styles.emptyText}>No hay movimientos aún</p>
        <p style={styles.emptyHint}>Usa los botones de arriba para registrar tu primer movimiento</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Movimientos</h2>
      <div style={styles.list}>
        {transactions.map((t, index) => (
          <div
            key={t.id}
            style={{
              ...styles.item,
              animationDelay: `${index * 0.05}s`,
            }}
            className="fade-in"
          >
            <div style={styles.left}>
              <div style={{
                ...styles.typeIcon,
                background: t.type === 'ingreso' ? 'var(--accent-green-bg)' : 'var(--accent-red-bg)',
                color: t.type === 'ingreso' ? 'var(--accent-green)' : 'var(--accent-red)',
              }}>
                {t.type === 'ingreso' ? '↑' : '↓'}
              </div>
              <div>
                <p style={styles.concept}>{t.concept}</p>
                <p style={styles.date}>{formatDate(t.date)}</p>
              </div>
            </div>
            <div style={styles.right}>
              <p style={{
                ...styles.amount,
                color: t.type === 'ingreso' ? 'var(--accent-green)' : 'var(--accent-red)',
              }}>
                {t.type === 'ingreso' ? '+' : '-'}{formatCurrency(t.amount)}
              </p>
              <button
                style={styles.deleteBtn}
                onClick={() => onDelete(t.id)}
                title="Eliminar"
              >
                ✕
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    flex: 1,
  },
  title: {
    fontSize: '18px',
    fontWeight: 700,
    color: 'var(--text-primary)',
    marginBottom: '12px',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    paddingBottom: '24px',
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '14px 16px',
    background: 'var(--bg-card)',
    borderRadius: 'var(--radius-sm)',
    border: '1px solid var(--border)',
  },
  left: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    flex: 1,
    minWidth: 0,
  },
  typeIcon: {
    width: '38px',
    height: '38px',
    borderRadius: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '18px',
    fontWeight: 700,
    flexShrink: 0,
  },
  concept: {
    fontSize: '15px',
    fontWeight: 500,
    color: 'var(--text-primary)',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    maxWidth: '160px',
  },
  date: {
    fontSize: '12px',
    color: 'var(--text-muted)',
    marginTop: '2px',
  },
  right: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    flexShrink: 0,
  },
  amount: {
    fontSize: '15px',
    fontWeight: 700,
    whiteSpace: 'nowrap',
  },
  deleteBtn: {
    background: 'transparent',
    color: 'var(--text-muted)',
    fontSize: '12px',
    padding: '6px',
    borderRadius: '6px',
    lineHeight: 1,
  },
  empty: {
    textAlign: 'center',
    padding: '48px 24px',
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyIcon: {
    fontSize: '48px',
    marginBottom: '16px',
  },
  emptyText: {
    fontSize: '17px',
    fontWeight: 600,
    color: 'var(--text-secondary)',
    marginBottom: '8px',
  },
  emptyHint: {
    fontSize: '14px',
    color: 'var(--text-muted)',
    maxWidth: '240px',
  },
};
