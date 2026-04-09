import { useState, useEffect, useCallback } from 'react'
import {
  fetchExpenses,
  fetchSummary,
  createExpense,
  updateExpense,
  deleteExpense,
} from '../api/expenses'
import type { Expense, ExpenseCreate, ExpenseUpdate, Summary } from '../types'

interface Filters {
  category?: string
  start_date?: string
  end_date?: string
}

export function useExpenses(filters: Filters = {}) {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [summary, setSummary] = useState<Summary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const filterKey = JSON.stringify(filters)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [exps, sum] = await Promise.all([
        fetchExpenses(filters),
        fetchSummary(),
      ])
      setExpenses(exps)
      setSummary(sum)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterKey])

  useEffect(() => {
    load()
  }, [load])

  const addExpense = async (payload: ExpenseCreate) => {
    const created = await createExpense(payload)
    await load()
    return created
  }

  const editExpense = async (id: number, payload: ExpenseUpdate) => {
    const updated = await updateExpense(id, payload)
    await load()
    return updated
  }

  const removeExpense = async (id: number) => {
    await deleteExpense(id)
    await load()
  }

  return {
    expenses,
    summary,
    loading,
    error,
    refetch: load,
    addExpense,
    editExpense,
    removeExpense,
  }
}
