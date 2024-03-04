import { useState} from "react"
import "./App.css";
// require('dotenv').config({path: '../.env'});
function App() {
  const [characters, setCharacters] = useState({});

  const host = process.env.REACT_APP_BACK_END_HOST || "127.0.0.1";
  const port = process.env.REACT_APP_BACK_END_PORT || 5000;


  const fetchCharacters = async () => {
    try {
      const response = await fetch(`http://${host}:${port}/characters`);
      const data = await response.json();
      setCharacters(data);
  } catch (error) {
    console.error('Error fetching characters:', error);
  }
}
return (
    <div className="App">
      <p>characters</p>
      <div>{JSON.stringify(characters)}</div>
      <button onClick={fetchCharacters}>Fetch Characters</button>
      
    </div>
  );
}
export default App;