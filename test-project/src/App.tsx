import { useState } from "react";
// import "./App.css";
// import Message from './Message';
import ListGroup from "./Components/ListGroup";

function App() {
  const [count, setCount] = useState(0);
  const items = ["New York", "Los Angeles", "London", "Delhi", "Goa"];

  const handleSelectedItem = (name: string) => {
    console.log(name);
  };

  return (
    <>
      <div>
        <ListGroup
          items={items}
          name="Cities"
          onSelectItem={handleSelectedItem}
        />
      </div>
    </>
  );
}

export default App;
