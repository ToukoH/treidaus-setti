import React from 'react'
import StockChart from './StockChart'

function App () {
  // Sample data (you would fetch this from an API in a real-world scenario)
  const data = [
    { date: '01-01-2023', price: 220 },
    { date: '02-01-2023', price: 230 },
    { date: '03-01-2023', price: 215 }
    // ... more data
  ]

  return (
    <div className="App">
      <h1>Stock Chart</h1>
      <StockChart data={data} />
    </div>
  )
}

export default App
