import { Fragment } from "react";
import { useState } from "react";
// import { MouseEvent } from "react";

interface inputs {
  name: string;
  items: string[];
  onSelectItem: (name: string) => void;
}

function ListGroup(inputs: inputs) {
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [name, setName] = useState("");

  const handleItemSelection = (item: string, index: number) => {
    setSelectedIndex(index);
    inputs.onSelectItem(item);
  };

  return (
    <Fragment>
      <h1>{inputs.name}</h1>
      <ul className="list-group">
        {inputs.items.map((item, index) => (
          <li
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            key={item}
            onClick={() => handleItemSelection(item, index)}
          >
            {item}
          </li>
        ))}
      </ul>
    </Fragment>
  );
}

export default ListGroup;
