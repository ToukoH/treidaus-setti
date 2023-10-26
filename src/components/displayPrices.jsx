import axios from 'axios'

const fetchAvailableFilenames = async () => {
    try {
        const url = 'http://127.0.0.1:8000/listJsonFiles'
        const response = await axios.get(url)
        return response.data
    } catch (error) {
        console.error('Error fetching available filenames:', error)
        return []
    }
}

const fetchJsonFile = async (filename) => {
    try {
        const url = `http://127.0.0.1:8000/getJsonFile/${filename}.json`
        const response = await axios.get(url)
        return response.data
    } catch (error) {
        console.error('Error fetching JSON file:', error)
        return null
    }
}

const fetchAndProcessFile = async () => {
    const filenames = await fetchAvailableFilenames()

    if (filenames.length > 0) {
    // For simplicity, we're just taking the first file in the list.
    // You might want to add some logic here to select the correct file.
        const filename = filenames[0].split('.')[0]

        const data = await fetchJsonFile(filename)
        if (data) {
            // Do something with the data
            console.log(data)
        }
    } else {
        console.log('No files available to fetch.')
    }
}

fetchAndProcessFile()
