import type { Expense } from '../types'
import { CATEGORY_EMOJI, CATEGORY_COLOR } from '../types'

interface Props {
  expenses: Expense[]
  onEdit: (expense: Expense) => void
  onDelete: (id: number) => void
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

function formatAmount(amount: number) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(amount)
}

export function ExpenseList({ expenses, onEdit, onDelete }: Props) {
  if (expenses.length === 0) {
    return (
      <div className="empty-state">
        <span className="empty-icon">🧾</span>
        <p>No expenses yet. Add your first one!</p>
      </div>
    )
  }

  return (
    <div className="expense-list">
      {expenses.map((exp) => (
        <div key={exp.id} className="expense-row">
          <div
            className="category-dot"
            style={{ background: CATEGORY_COLOR[exp.category] }}
          >
            {CATEGORY_EMOJI[exp.category]}
          </div>
          <div className="expense-info">
            <span className="expense-desc">{exp.description}</span>
            <span className="expense-meta">
              {formatDate(exp.date)}
              {exp.note && <span className="expense-note"> · {exp.note}</span>}
              {exp.ai_categorized && (
                <span className="ai-badge" title="Category suggested by AI">✨ AI</span>
              )}
            </span>
          </div>
          <div className="expense-right">
            <span className="expense-amount">{formatAmount(exp.amount)}</span>
            <span
              className="category-chip"
              style={{ borderColor: CATEGORY_COLOR[exp.category], color: CATEGORY_COLOR[exp.category] }}
            >
              {exp.category}
            </span>
            <div className="expense-actions">
              <button className="action-btn" onClick={() => onEdit(exp)} title="Edit">✏️</button>
              <button className="action-btn danger" onClick={() => onDelete(exp.id)} title="Delete">🗑️</button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
