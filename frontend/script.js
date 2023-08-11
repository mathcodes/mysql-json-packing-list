loadPackingList()

function createItemPrompt() {
  // Prompt the user for item details
  const itemType = prompt("Enter item type:");
  const itemName = prompt("Enter item name:");
  const quantity = prompt("Enter quantity:");
  const colors = prompt("Enter colors:");
  const importance = prompt("Enter importance:");
  const complete = prompt("Complete yet?: (true/false)");

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
          importance: importance,
          complete: complete
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

document.addEventListener("DOMContentLoaded", function () {
  loadPackingList();
});

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
        // Create a class variable based on completeness
        const completenessClass = item.complete ? 'bg-blue-500' : 'bg-purple-300';
        // Add classes to the itemRow element
        itemRow.classList.add('py-2', 'px-4', 'rounded', completenessClass);
        itemRow.innerHTML = `
          <td class="text-center">${item.item_type}</td>
          <td class="text-center">${item.item_name}</td>
          <td class="text-center">${item.quantity}</td>
          <td class="text-center">${item.colors}</td>
          <td class="text-center">${item.importance}</td>
          <td class="text-center">

          ${item.complete ? 'Yes' : 'No'}
          </td>
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

