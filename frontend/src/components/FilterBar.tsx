import { CATEGORIES, CATEGORY_EMOJI } from '../types'
import type { Category } from '../types'

interface Filters {
  category?: string
  start_date?: string
  end_date?: string
}

interface Props {
  filters: Filters
  onChange: (f: Filters) => void
}

export function FilterBar({ filters, onChange }: Props) {
  return (
    <div className="filter-bar">
      <select
        className="filter-select"
        value={filters.category ?? ''}
        onChange={(e) =>
          onChange({ ...filters, category: e.target.value || undefined })
        }
      >
        <option value="">All Categories</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>
            {CATEGORY_EMOJI[c]} {c}
          </option>
        ))}
      </select>

      <input
        className="filter-input"
        type="date"
        value={filters.start_date ?? ''}
        onChange={(e) =>
          onChange({ ...filters, start_date: e.target.value || undefined })
        }
        placeholder="From"
        title="From date"
      />

      <input
        className="filter-input"
        type="date"
        value={filters.end_date ?? ''}
        onChange={(e) =>
          onChange({ ...filters, end_date: e.target.value || undefined })
        }
        placeholder="To"
        title="To date"
      />

      {(filters.category || filters.start_date || filters.end_date) && (
        <button
          className="btn-clear"
          onClick={() => onChange({})}
        >
          Clear filters
        </button>
      )}
    </div>
  )
}
