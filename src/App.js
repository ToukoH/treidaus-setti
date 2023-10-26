import React from 'react'
import StockChart from './components/StockChart'
import TickerInput from './components/TickerInput'
import PricesTable from './components/PricesTable'

function App () {
    return (
        <div className="App">
            <TickerInput />
            <PricesTable />
        </div>
    )
}

export default App
