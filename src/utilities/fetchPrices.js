import axios from 'axios'

const fetchJsonFiles = async () => {
    try {
        const url = 'http://127.0.0.1:8000/listJsonFiles'
        const response = await axios.get(url)
        return response.data
    } catch (error) {
        console.error('Error fetching available filenames:', error)
        return []
    }
}

const fetchForFile = async (filename) => {
    try {
        const url = `http://127.0.0.1:8000/getJsonFile/${filename}.json`
        const response = await axios.get(url)
        return response.data
    } catch (error) {
        console.error('Error fetching JSON file:', error)
        return null
    }
}

const getFile = async (filename) => {
    const filenames = await fetchJsonFiles()

    if (filenames.length > 0) {
        const data = await fetchForFile(filename)
        if (data) {
            res = data
            console.log(data)
        }
    } else {
        console.log('No files available to fetch.')
    }
}

export let res
export default getFile
