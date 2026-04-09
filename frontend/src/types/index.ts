// All shared TypeScript types — single source of truth for shape contracts

export type Category =
  | 'FOOD'
  | 'TRANSPORT'
  | 'HOUSING'
  | 'HEALTH'
  | 'ENTERTAINMENT'
  | 'SHOPPING'
  | 'UTILITIES'
  | 'OTHER'

export const CATEGORIES: Category[] = [
  'FOOD', 'TRANSPORT', 'HOUSING', 'HEALTH',
  'ENTERTAINMENT', 'SHOPPING', 'UTILITIES', 'OTHER',
]

export const CATEGORY_EMOJI: Record<Category, string> = {
  FOOD: '🍜',
  TRANSPORT: '🚌',
  HOUSING: '🏠',
  HEALTH: '💊',
  ENTERTAINMENT: '🎬',
  SHOPPING: '🛍️',
  UTILITIES: '💡',
  OTHER: '📦',
}

export const CATEGORY_COLOR: Record<Category, string> = {
  FOOD: '#f97316',
  TRANSPORT: '#3b82f6',
  HOUSING: '#8b5cf6',
  HEALTH: '#10b981',
  ENTERTAINMENT: '#ec4899',
  SHOPPING: '#f59e0b',
  UTILITIES: '#6366f1',
  OTHER: '#6b7280',
}

export interface Expense {
  id: number
  description: string
  amount_cents: number
  amount: number
  category: Category
  date: string
  note: string | null
  ai_categorized: boolean
}

export interface ExpenseCreate {
  description: string
  amount: number
  category?: Category
  date: string
  note?: string
}

export interface ExpenseUpdate {
  description?: string
  amount?: number
  category?: Category
  date?: string
  note?: string
}

export interface CategorySummary {
  category: Category
  total_cents: number
  total: number
}

export interface Summary {
  by_category: CategorySummary[]
  grand_total_cents: number
  grand_total: number
  count: number
}

export interface ApiResponse<T> {
  data: T | null
  error: string | null
}
