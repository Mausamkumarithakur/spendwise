import { useState } from 'react'
import { useExpenses } from './hooks/useExpenses'
import { ExpenseForm } from './components/ExpenseForm'
import { ExpenseList } from './components/ExpenseList'
import { Dashboard } from './components/Dashboard'
import { FilterBar } from './components/FilterBar'
import type { Expense, ExpenseCreate } from './types'
import './App.css'

type Tab = 'expenses' | 'dashboard'

interface Filters {
  category?: string
  start_date?: string
  end_date?: string
}

export default function App() {
  const [tab, setTab] = useState<Tab>('expenses')
  const [filters, setFilters] = useState<Filters>({})
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<Expense | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)

  const { expenses, summary, loading, error, addExpense, editExpense, removeExpense } =
    useExpenses(filters)

  const handleAdd = async (payload: ExpenseCreate) => {
    setActionError(null)
    await addExpense(payload)
    setShowForm(false)
  }

  const handleEdit = async (payload: ExpenseCreate) => {
    if (!editing) return
    setActionError(null)
    await editExpense(editing.id, payload)
    setEditing(null)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this expense?')) return
    try {
      setActionError(null)
      await removeExpense(id)
    } catch (e) {
      setActionError(e instanceof Error ? e.message : 'Delete failed')
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">💸</span>
            <span className="logo-text">Spendwise</span>
          </div>
          <nav className="tab-nav">
            <button
              className={`tab-btn ${tab === 'expenses' ? 'active' : ''}`}
              onClick={() => setTab('expenses')}
            >
              Expenses
            </button>
            <button
              className={`tab-btn ${tab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setTab('dashboard')}
            >
              Dashboard
            </button>
          </nav>
          <button className="btn-primary add-btn" onClick={() => setShowForm(true)}>
            + Add
          </button>
        </div>
      </header>

      <main className="app-main">
        {(error || actionError) && (
          <div className="global-error">{error ?? actionError}</div>
        )}

        {tab === 'dashboard' && summary && <Dashboard summary={summary} />}

        {tab === 'expenses' && (
          <>
            <FilterBar filters={filters} onChange={setFilters} />
            {loading ? (
              <div className="loading-state">Loading expenses...</div>
            ) : (
              <ExpenseList
                expenses={expenses}
                onEdit={(exp) => setEditing(exp)}
                onDelete={handleDelete}
              />
            )}
          </>
        )}
      </main>

      {(showForm || editing) && (
        <ExpenseForm
          onSubmit={editing ? handleEdit : handleAdd}
          onCancel={() => {
            setShowForm(false)
            setEditing(null)
          }}
          initial={editing ?? undefined}
        />
      )}
    </div>
  )
}
