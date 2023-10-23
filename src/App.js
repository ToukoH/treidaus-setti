import React from 'react'
import StockChart from './StockChart'
import axios from 'axios'

const url = 'http://127.0.0.1:8000/getJsonFile/pliisom.json'

axios({
  method: 'get',
  url
}).then(function (response) {
  console.log(response.data)
}).catch(function (error) {
  console.error('Error fetching data: ', error)
})

function App () {
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
