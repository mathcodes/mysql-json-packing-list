loadPackingList()

function createItemPrompt() {
  // Prompt the user for item details
  const itemType = prompt("Enter item type:");
  const itemName = prompt("Enter item name:");
  const quantity = prompt("Enter quantity:");
  const colors = prompt("Enter colors:");
  const importance = prompt("Enter importance:");

  // Call the API endpoint to create the item
  fetch('/create', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          item_type: itemType,
          item_name: itemName,
          quantity: quantity,
          colors: colors,
          importance: importance
      })
  })
  .then(response => response.json())
  .then(data => {

      // Handle success
      alert("Item created successfully!");
  })
  .catch(error => {
      // Handle error
      console.error("Error creating item:", error);
  });
}

function loadPackingList() {
  // Call the API endpoint to get the list of items
  fetch('/list', {
      method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
      // Populate the itemTypes div with the data
      const itemTypesRow = document.getElementById('itemTypes');
      itemTypesRow.innerHTML = ""; // Clear existing items
      for (let category in data) {
          data[category].forEach(item => {
              // Create a new row for each item and add to the itemTypes row
              const itemRow = document.createElement('tr');
              itemRow.innerHTML = `
                  <td>${item.item_type}</td>
                  <td>${item.item_name}</td>
                  <td>${item.quantity}</td>
                  <td>${item.colors}</td>
                  <td>${item.importance}</td>
              `;
              itemTypesRow.appendChild(itemRow);
          });
      }
  })
  .catch(error => {
      // Handle error
      console.error("Error loading packing list:", error);
  });
}

