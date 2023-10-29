import React, { useEffect, useState } from 'react'
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts'
import { Box, Heading } from '@chakra-ui/react'
import { res } from '../utilities/fetchPrices'

const StockChart = () => {
    const [chartData, setChartData] = useState([])

    useEffect(() => {
        if (res && Object.keys(res).length > 0) {
            const formattedData = Object.entries(res).map(([date, data]) => {
                return {
                    date: date.substring(0, 10),
                    close: data.Close
                }
            })
            setChartData(formattedData)
        }
    }, [res])

    return (
        <div className="container full-width">
            <Box
                borderWidth='1px'
                borderRadius='lg'
                overflow='hidden'
                p={4} ml={8} mt={5} mr={8}>
                <Heading
                    size="md"
                    mb={4}>
                    Stock Chart
                </Heading>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart
                        data={chartData}
                        margin={{
                            top: 5,
                            right: 30,
                            left: 20,
                            bottom: 5
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="close"
                            stroke="#8884d8"
                            activeDot={{ r: 8 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </Box>
        </div>
    )
}

export default StockChart
