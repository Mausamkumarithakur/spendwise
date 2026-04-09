import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import type { Summary } from '../types'
import { CATEGORY_COLOR, CATEGORY_EMOJI } from '../types'

interface Props {
  summary: Summary
}

function formatINR(amount: number) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount)
}

export function Dashboard({ summary }: Props) {
  const chartData = summary.by_category
    .filter((c) => c.total_cents > 0)
    .map((c) => ({
      name: c.category,
      value: c.total,
      color: CATEGORY_COLOR[c.category],
    }))

  const top = [...summary.by_category]
    .sort((a, b) => b.total_cents - a.total_cents)
    .slice(0, 4)
    .filter((c) => c.total_cents > 0)

  return (
    <div className="dashboard">
      <div className="stat-row">
        <div className="stat-card">
          <span className="stat-label">Total Spent</span>
          <span className="stat-value">{formatINR(summary.grand_total)}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Transactions</span>
          <span className="stat-value">{summary.count}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Avg per Transaction</span>
          <span className="stat-value">
            {summary.count > 0 ? formatINR(summary.grand_total / summary.count) : '—'}
          </span>
        </div>
      </div>

      {chartData.length > 0 && (
        <div className="chart-section">
          <h3 className="section-label">Spending by Category</h3>
          <div className="chart-layout">
            <ResponsiveContainer width="50%" height={220}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={90}
                  dataKey="value"
                  paddingAngle={3}
                >
                  {chartData.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => formatINR(v)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>

            <div className="top-categories">
              {top.map((c) => (
                <div key={c.category} className="top-cat-row">
                  <span className="top-cat-emoji">{CATEGORY_EMOJI[c.category]}</span>
                  <span className="top-cat-name">{c.category}</span>
                  <span className="top-cat-amount">{formatINR(c.total)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
