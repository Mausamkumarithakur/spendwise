/**
 * API client — all fetch calls live here.
 * Components never call fetch directly; they use these functions.
 */
import type { Expense, ExpenseCreate, ExpenseUpdate, Summary, ApiResponse } from '../types'

const BASE = '/api/expenses'

async function request<T>(
  url: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const body: ApiResponse<T> = await res.json()
  if (body.error) throw new Error(body.error)
  return body.data as T
}

export async function fetchExpenses(params?: {
  category?: string
  start_date?: string
  end_date?: string
}): Promise<Expense[]> {
  const qs = new URLSearchParams()
  if (params?.category) qs.set('category', params.category)
  if (params?.start_date) qs.set('start_date', params.start_date)
  if (params?.end_date) qs.set('end_date', params.end_date)
  const query = qs.toString() ? `?${qs}` : ''
  return request<Expense[]>(`${BASE}/${query}`)
}

export async function createExpense(payload: ExpenseCreate): Promise<Expense> {
  return request<Expense>(`${BASE}/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateExpense(id: number, payload: ExpenseUpdate): Promise<Expense> {
  return request<Expense>(`${BASE}/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export async function deleteExpense(id: number): Promise<void> {
  await request(`${BASE}/${id}`, { method: 'DELETE' })
}

export async function fetchSummary(): Promise<Summary> {
  return request<Summary>(`${BASE}/summary`)
}
