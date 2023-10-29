import React, { useState } from 'react'
import { Box, Input, Heading, Button, InputGroup, Select } from '@chakra-ui/react'
import Axios from 'axios'
import CreateId from '../utilities/createId'
import getFile from '../utilities/fetchPrices'

function TickerInput () {
    const [tickerInputNameField, setTickerInputNameField] = useState('')
    const [tickerInputStartDate, setTickerInputStartDate] = useState('')
    const [tickerInputInterval, setTickerInputInterval] = useState('')
    const [tickerInputEndDate, setTickerInputEndDate] = useState('')

    const handleTickerNameChange = (event) => {
        setTickerInputNameField(event.target.value)
    }
    const handleStartDateChange = (event) => {
        setTickerInputStartDate(event.target.value)
    }

    const handleInputIntervalChange = (event) => {
        setTickerInputInterval(event.target.value)
    }

    const handleEndDateChange = (event) => {
        setTickerInputEndDate(event.target.value)
    }

    const handleSubmit = async () => {
        const id = CreateId(6)
        const url = `http://127.0.0.1:8000/writeFile/${id}.json`

        const postTemplate = {
            TICKER: tickerInputNameField,
            START_DATE: tickerInputStartDate,
            END_DATE: tickerInputEndDate,
            INTERVAL: tickerInputInterval,
            CLEAR: false
        }

        const data = JSON.stringify(postTemplate)
        console.log(data)
        console.log(url)

        try {
            const response = await Axios.post(url, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            console.log('Response:', response.data)
            const filename = `${id}.json`
            const res = getFile(filename)
            console.log(res)
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
                    value={tickerInputNameField}
                    onChange={handleTickerNameChange}
                    mt={2}
                />
                <InputGroup mt={1}>
                    <Input
                        type='date'
                        value={tickerInputStartDate}
                        onChange={handleStartDateChange}
                    />
                    <Input
                        type='date'
                        value={tickerInputEndDate}
                        onChange={handleEndDateChange}
                    />
                </InputGroup>
                <Select
                    placeholder='Select interval' mt={1}
                    value={tickerInputInterval}
                    onChange={handleInputIntervalChange}>
                    <option value='1m'>1m</option>
                    <option value='90m'>90m</option>
                    <option value='1d'>1d</option>
                </Select>
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
