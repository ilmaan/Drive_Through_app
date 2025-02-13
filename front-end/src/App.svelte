<script>
	import { onMount } from 'svelte';
	let orderText = '';
	let totalItems = 0;
	let activeOrders = [];
	let canceledOrders = [];
	let totalBurgers = 0;
	let totalFries = 0;
	let totalDrinks = 0;
  
	let mediaRecorder;
	let audioChunks = [];
	let isRecording = false;
  
	let recognition;
  
	async function fetchOrders() {
	  try {
		const response = await fetch('http://localhost:8100/orders/all');
		const data = await response.json();
		console.log("DATRA",data);
		activeOrders = data.active_orders;
		canceledOrders = data.canceled_orders;
		totalItems = activeOrders.reduce((sum, order) => sum + Object.values(order.order_items).reduce((a, b) => a + b, 0), 0);
		
		// Calculate total burgers, fries, and drinks
		totalBurgers = activeOrders.reduce((sum, order) => sum + (order.order_items.burger || 0), 0);
		totalFries = activeOrders.reduce((sum, order) => sum + (order.order_items.fries || 0), 0);
		totalDrinks = activeOrders.reduce((sum, order) => sum + (order.order_items.drink || 0), 0);
	  } catch (error) {
		console.error('Error fetching orders:', error);
	  }
	}
  
	function validateOrderText(text) {
		// Check if the order text is not empty
		if (!text.trim()) {
			alert('Order text cannot be empty.');
			return false;
		}

		// Example: Check if the order contains at least one of the keywords
		const validKeywords = ['burger', 'fries', 'drink','cancel','burgers','drinks'];
		const containsValidKeyword = validKeywords.some(keyword => text.toLowerCase().includes(keyword));

		if (!containsValidKeyword) {
			alert('Order must contain at least one valid item: burger, fries, or drink.');
			return false;
		}

		return true;
	}
  
	async function placeOrder() {
		if (!validateOrderText(orderText)) {
			return; // Exit if validation fails
		}

		try {
			const response = await fetch('http://127.0.0.1:8100/process_input/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ order_text: orderText })
			});
			
			console.log("response----->>>>",response);
			const data = await response.json();
			console.log("data--+++++--->>>>",data);
			if (response.ok) {
			  alert(`Order placed successfully\n order number: ${data.order_no} \n order items: \n Burgers: ${data.order_items.burger} \n Drinks:${data.order_items.drink} \n Fries ${data.order_items.fries} `); 
			  console.log(`Order placed successfully\n order number: ${data.order_no} \n order items:\n Burgers: ${JSON.stringify(data.order_items)}`);
			  orderText = '';
			  fetchOrders();
			} else if (response.status === 400) {
			  const errorData = await response.json();
			  alert(errorData.detail); // Display the alert message
			}
			else {
			  alert('Hello, Please order something! from the menu we have.');
			}
		} catch (error) {
			console.error('Error placing order:', error);
		}
	}
  
	function startRecording() {
		if (!('webkitSpeechRecognition' in window)) {
			alert('Speech recognition not supported in this browser.');
			return;
		}

		recognition = new webkitSpeechRecognition();
		recognition.interimResults = true;
		recognition.lang = 'en-US';

		recognition.onresult = (event) => {
			const transcript = Array.from(event.results)
				.map(result => result[0])
				.map(result => result.transcript)
				.join('');
			orderText = transcript; // Set the recognized text to orderText
		};

		recognition.onerror = (event) => {
			console.error('Speech recognition error:', event.error);
		};

		recognition.start();
		isRecording = true; // Update recording state
	}

	function stopRecording() {
		if (recognition) {
			recognition.stop();
			isRecording = false; // Update recording state
		}
	}

	function handleMouseUp() {
		stopRecording(); // Stop recording when the mouse is released
		placeOrder(); // Submit the order
	}
  
	onMount(fetchOrders);
  </script>
  
  <main>
	<h1>Drive-Through Orders</h1>
	<p><strong>Total Items Ordered:</strong> {totalItems}</p>
	<p><strong>Total Burgers:</strong> {totalBurgers}</p>
	<p><strong>Total Fries:</strong> {totalFries}</p>
	<p><strong>Total Drinks:</strong> {totalDrinks}</p>

	<h2>Place a New Order</h2>
	<input type="text" bind:value={orderText} placeholder="Enter order details..." />
	<button on:click={placeOrder}>Submit Order</button>
	
	<button 
		on:mousedown={startRecording} 
		on:mouseup={handleMouseUp}
	>
		{isRecording ? 'Recording...' : 'Hold to Record'}
	</button>
	
	<h2>Active Orders</h2>
	<table class="active-orders">
		<thead>
			<tr>
				<th>Order No</th>
				<th>Burgers <i class="fas fa-hamburger"></i></th>
				<th>Fries <i class="fas fa-french-fries"></i></th>
				<th>Drinks <i class="fas fa-coffee"></i></th>
			</tr>
		</thead>
		<tbody>
			{#each activeOrders as order}
				<tr>
					<td>{order.order_no}</td>
					<td>{order.order_items.burger || 0}</td>
					<td>{order.order_items.fries || 0}</td>
					<td>{order.order_items.drink || 0}</td>
				</tr>
			{/each}
		</tbody>
	</table>
  
	<h2>Canceled Orders</h2>
	<table class="canceled-orders">
		<thead>
			<tr>
				<th>Order No</th>
				<th>Burgers <i class="fas fa-hamburger"></i></th>
				<th>Fries <i class="fas fa-french-fries"></i></th>
				<th>Drinks <i class="fas fa-coffee"></i></th>
			</tr>
		</thead>
		<tbody>
			{#each canceledOrders as order}
				<tr>
					<td>{order.order_no}</td>
					<td>{order.order_items.burgers || 0}</td>
					<td>{order.order_items.fries || 0}</td>
					<td>{order.order_items.drinks || 0}</td>
				</tr>
			{/each}
		</tbody>
	</table>
  

  
	
  </main>
  












  
  <style>
	main {
	  max-width: 600px;
	  margin: auto;
	  font-family: Arial, sans-serif;
	}
	h1, h2 {
	  text-align: center;
	}
	ul {
	  list-style-type: none;
	  padding: 0;
	}
	li {
	  background: #f4f4f4;
	  margin: 5px 0;
	  padding: 10px;
	  border-radius: 5px;
	}
	input {
	  width: 100%;
	  padding: 8px;
	  margin-top: 10px;
	}
	button {
	  display: inline-block;
	  width: auto;
	  padding: 10px;
	  background: #007bff;
	  color: white;
	  border: none;
	  margin-top: 10px;
	  cursor: pointer;
	}
	button:hover {
	  background: #0056b3;
	}
	button:active {
	  background: red;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		margin-top: 20px;
	}
	th, td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: center;
	}
	th {
		background-color: #f2f2f2;
	}
	tr:nth-child(even) {
		background-color: #f9f9f9;
	}
	tr:hover {
		background-color: #ddd;
	}
	/* Make the Order No column dark */
	th:first-child, td:first-child {
		background-color: #333;
		color: black;
		font-weight: bold;

	}
	/* Active Orders Table */
	.active-orders th, .active-orders td {
		background-color: lightgreen; /* Light green background */
	}
	/* Canceled Orders Table */
	.canceled-orders th, .canceled-orders td {
		background-color: palevioletred; /* Light red background */
	}
	/* Change button color to red when recording */
	.is-recording {
	  background: red;
	}
  </style>
	