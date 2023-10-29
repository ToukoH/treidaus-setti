import React from 'react'
import getFile from '../utilities/fetchPrices'
import { Button, Box, Heading } from '@chakra-ui/react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function PricesTable () {
    const handlePress = async () => {
        getFile()
    }

    return (
        <div className='ticker-container'>
            <Box>
                <Button onClick={handlePress}>Get</Button>
            </Box>
        </div>
    )
}

export default PricesTable
