import { useState } from 'react'
import type { ExpenseCreate, Expense, Category } from '../types'
import { CATEGORIES, CATEGORY_EMOJI } from '../types'

interface Props {
  onSubmit: (payload: ExpenseCreate) => Promise<void>
  onCancel: () => void
  initial?: Expense
}

const today = () => new Date().toISOString().slice(0, 10)

export function ExpenseForm({ onSubmit, onCancel, initial }: Props) {
  const [description, setDescription] = useState(initial?.description ?? '')
  const [amount, setAmount] = useState(initial ? String(initial.amount) : '')
  const [category, setCategory] = useState<Category | ''>(initial?.category ?? '')
  const [date, setDate] = useState(initial?.date ?? today())
  const [note, setNote] = useState(initial?.note ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  const handleSubmit = async () => {
    if (!description.trim()) return setFormError('Description is required')
    const amt = parseFloat(amount)
    if (isNaN(amt) || amt <= 0) return setFormError('Enter a valid positive amount')
    if (!date) return setFormError('Date is required')
    setFormError(null)
    setSubmitting(true)
    try {
      const payload: ExpenseCreate = {
        description: description.trim(),
        amount: amt,
        date,
        ...(category ? { category: category as Category } : {}),
        note: note.trim(),
      }
      await onSubmit(payload)
    } catch (e) {
      setFormError(e instanceof Error ? e.message : 'Failed to save expense')
      setSubmitting(false)
    }
  }

  return (
    <div className="form-overlay">
      <div className="form-card">
        <h2 className="form-title">{initial ? 'Edit Expense' : 'New Expense'}</h2>

        {formError && <div className="form-error">{formError}</div>}

        <label className="field-label">Description *</label>
        <input
          className="field-input"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g. Lunch at Cafe"
        />

        <label className="field-label">Amount (Rs) *</label>
        <input
          className="field-input"
          type="number"
          min="0.01"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="0.00"
        />

        <label className="field-label">Category</label>
        <select
          className="field-input"
          value={category}
          onChange={(e) => setCategory(e.target.value as Category | '')}
        >
          <option value="">Auto-detect with AI</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {CATEGORY_EMOJI[c]} {c}
            </option>
          ))}
        </select>

        <label className="field-label">Date *</label>
        <input
          className="field-input"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />

        <label className="field-label">Note (optional)</label>
        <input
          className="field-input"
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Any extra details"
        />

        <div className="form-actions">
          <button className="btn-secondary" onClick={onCancel} disabled={submitting}>
            Cancel
          </button>
          <button className="btn-primary" onClick={handleSubmit} disabled={submitting}>
            {submitting ? 'Saving...' : initial ? 'Update' : 'Add Expense'}
          </button>
        </div>
      </div>
    </div>
  )
}