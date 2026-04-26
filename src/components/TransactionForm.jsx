import { useState, useRef, useEffect } from 'react';
import { formatCurrency } from '../utils/format';

export default function TransactionForm({ type, onSave, onCancel }) {
  const [amount, setAmount] = useState('');
  const [concept, setConcept] = useState('');
  const amountRef = useRef(null);

  useEffect(() => {
    if (amountRef.current) {
      amountRef.current.focus();
    }
  }, []);

  const isIncome = type === 'ingreso';
  const accentColor = isIncome ? 'var(--accent-green)' : 'var(--accent-red)';
  const accentBg = isIncome ? 'var(--accent-green-bg)' : 'var(--accent-red-bg)';

  const handleSubmit = (e) => {
    e.preventDefault();
    const numAmount = parseFloat(amount);
    if (!numAmount || numAmount <= 0 || !concept.trim()) return;
    onSave(type, numAmount, concept.trim());
  };

  const isValid = parseFloat(amount) > 0 && concept.trim().length > 0;

  return (
    <div style={styles.overlay} onClick={onCancel}>
      <div
        style={styles.modal}
        className="slide-up"
        onClick={(e) => e.stopPropagation()}
      >
        <div style={styles.header}>
          <div style={{
            ...styles.typeLabel,
            background: accentBg,
            color: accentColor,
          }}>
            {isIncome ? '+ Ingreso' : '− Egreso'}
          </div>
          <button style={styles.closeBtn} onClick={onCancel}>✕</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={styles.amountSection}>
            <label style={styles.label}>Monto</label>
            <div style={styles.amountInputWrap}>
              <span style={{ ...styles.currencySign, color: accentColor }}>$</span>
              <input
                ref={amountRef}
                type="number"
                inputMode="decimal"
                step="0.01"
                min="0"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                style={styles.amountInput}
              />
            </div>
            {amount && parseFloat(amount) > 0 && (
              <p style={{ ...styles.preview, color: accentColor }}>
                {isIncome ? '+' : '-'}{formatCurrency(parseFloat(amount))}
              </p>
            )}
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Concepto</label>
            <input
              type="text"
              placeholder={isIncome ? 'Ej: Venta de repuesto' : 'Ej: Compra de materiales'}
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              style={styles.textInput}
              maxLength={100}
            />
          </div>

          <button
            type="submit"
            disabled={!isValid}
            style={{
              ...styles.submitBtn,
              background: isValid ? accentColor : 'var(--bg-card)',
              color: isValid ? '#fff' : 'var(--text-muted)',
              opacity: isValid ? 1 : 0.6,
            }}
          >
            Guardar {isIncome ? 'Ingreso' : 'Egreso'}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: 'fixed',
    inset: 0,
    background: 'rgba(0, 0, 0, 0.6)',
    backdropFilter: 'blur(4px)',
    display: 'flex',
    alignItems: 'flex-end',
    justifyContent: 'center',
    zIndex: 1000,
    padding: '16px',
  },
  modal: {
    background: 'var(--bg-secondary)',
    borderRadius: '20px 20px 16px 16px',
    padding: '24px',
    width: '100%',
    maxWidth: '480px',
    border: '1px solid var(--border)',
    boxShadow: '0 -8px 40px rgba(0, 0, 0, 0.4)',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '24px',
  },
  typeLabel: {
    padding: '8px 16px',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: 700,
  },
  closeBtn: {
    background: 'var(--bg-card)',
    color: 'var(--text-secondary)',
    width: '36px',
    height: '36px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
  },
  amountSection: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '13px',
    fontWeight: 600,
    color: 'var(--text-secondary)',
    marginBottom: '8px',
    textTransform: 'uppercase',
    letterSpacing: '1px',
  },
  amountInputWrap: {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    background: 'var(--bg-card)',
    borderRadius: 'var(--radius-sm)',
    padding: '14px 16px',
    border: '1px solid var(--border)',
  },
  currencySign: {
    fontSize: '28px',
    fontWeight: 700,
  },
  amountInput: {
    flex: 1,
    fontSize: '28px',
    fontWeight: 700,
    color: 'var(--text-primary)',
    background: 'transparent',
    width: '100%',
  },
  preview: {
    fontSize: '13px',
    fontWeight: 600,
    marginTop: '8px',
    paddingLeft: '4px',
  },
  field: {
    marginBottom: '24px',
  },
  textInput: {
    width: '100%',
    padding: '14px 16px',
    fontSize: '16px',
    color: 'var(--text-primary)',
    background: 'var(--bg-card)',
    borderRadius: 'var(--radius-sm)',
    border: '1px solid var(--border)',
  },
  submitBtn: {
    width: '100%',
    padding: '16px',
    borderRadius: 'var(--radius-sm)',
    fontSize: '16px',
    fontWeight: 700,
    letterSpacing: '0.5px',
  },
};
