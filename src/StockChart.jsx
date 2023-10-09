import React from 'react'
import { LineChart, Line, XAxis, CartesianGrid } from 'recharts'

// eslint-disable-next-line react/prop-types
const StockChart = ({ data }) => {
  return (
    <LineChart
      width={500}
      height={300}
      data={data}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <Line type="monotone" dataKey="price" stroke="#8884d8" activeDot={{ r: 8 }} />
    </LineChart>
  )
}

export default StockChart
