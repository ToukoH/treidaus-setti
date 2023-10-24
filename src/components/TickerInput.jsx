import React, { useState } from 'react'
import { Box, Input, Heading, Button } from '@chakra-ui/react'

function TickerInput () {
    const [tickerInputField, setTickerInputField] = useState('')

    const handleChange = (event) => {
        setTickerInputField(event.target.value)
    }

    const handleSubmit = (event) => {
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
                    Set Ticker
                </Heading>
                <Input
                    placeholder='Ticker name'
                    value={tickerInputField}
                    onChange={handleChange}
                    mt={2}
                />
                <Button
                    colorScheme='blue'
                    mt={1}>
                    Submit
                </Button>
            </Box>
        </div>
    )
}

export default TickerInput
