import React from 'react'
import StockChart from './StockChart'

function App () {
  // NEXT TRY TO FETCH DATA FROM API AND USE IT HERE
  const data = [
    { date: '01-01-2023', price: 220 },
    { date: '02-01-2023', price: 230 },
    { date: '03-01-2023', price: 215 }
  ]

  return (
    <div className="App">
      <h1>Stock Chart</h1>
      <StockChart data={data} />
    </div>
  )
}

export default App
