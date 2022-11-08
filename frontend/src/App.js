import './App.css';
import { useState } from "react";

function App() {
  const [inputs, setInputs] = useState({});

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(encodeURIComponent(inputs.url))
    fetch('http://127.0.0.1:5000/recipe/' + encodeURIComponent(inputs.url))
       .then((response) => response.json())
       .then((data) => {
          console.log(data);
       })
       .catch((err) => {
          console.log(err.message);
       });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>URL:
      <input 
        type="text" 
        name="url" 
        value={inputs.url || ""} 
        onChange={handleChange}
      />
      </label>
    </form>
  )
}

export default App;
