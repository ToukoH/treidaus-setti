import React from 'react'
import getFile from '../utilities/fetchPrices'
import { Button, Box, Heading } from '@chakra-ui/react'

function PricesTable () {
    const handlePress = async () => {
        getFile()
    }

    return (
        <div className='ticker-container'>
            <Box
                maxW='sm'
                borderWidth='1px'
                borderRadius='lg'
                overflow='hidden'
                p={4} ml={8} mt={5}>
                <Heading
                    size="md"
                    mb={4}>
                    Prices
                </Heading>
            </Box>
        </div>
    )
}

export default PricesTable
