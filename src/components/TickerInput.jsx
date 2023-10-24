import React, { useState } from 'react'
import { Box, Input, Heading, Button } from '@chakra-ui/react'
import Axios from 'axios'

function makeId (length) {
    let result = ''
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    const charactersLength = characters.length
    let counter = 0
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength))
        counter += 1
    }
    return result
}

function TickerInput () {
    const [tickerInputField, setTickerInputField] = useState('')

    const handleChange = (event) => {
        setTickerInputField(event.target.value)
    }

    const handleSubmit = async () => {
        const id = makeId(6)
        const url = `http://127.0.0.1:8000/writeFile/${id}.json`

        const dataObj = JSON.parse('{"str_contents": "{\\"TICKER\\":\\"AAPL\\", \\"INTERVAL\\":\\"1d\\", \\"PERIOD\\":\\"1mo\\"}"}')
        const contentsObj = JSON.parse(dataObj.str_contents)
        contentsObj.TICKER = tickerInputField
        dataObj.str_contents = JSON.stringify(contentsObj)
        const data = JSON.stringify(dataObj)
        console.log(url)

        try {
            const response = await Axios.post(url, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            console.log('Response:', response.data)
        } catch (error) {
            console.error('Error posting data:', error)
        }
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
                    mt={1}
                    onClick={handleSubmit}>
                    Submit
                </Button>
            </Box>
        </div>
    )
}

export default TickerInput
