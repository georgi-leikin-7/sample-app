import {useEffect, useState} from 'react'
import './App.css'
import {ApiResponse, create} from "apisauce";

type Data = {
  message: string;
}

const apiClient = create({
  baseURL: "http://localhost:4566",
})

function App() {
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const response: ApiResponse<Data> = await apiClient.get("/index");

      if (response.ok && response.data) {
        setData(response.data || "No data available.");
      } else {
        console.log(response);
        setError(response.problem || "Unknown error.");
      }
    };
    fetchData();
  }, [])

  return (
    <>
      {data ? <p>Message: {data?.message}</p> : <p>Error: {error}</p>}
    </>
  )
}

export default App
