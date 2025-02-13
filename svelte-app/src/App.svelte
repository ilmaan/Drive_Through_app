<script>
  import { onMount } from 'svelte';
  let orderText = '';
  let totalItems = 0;
  let activeOrders = [];
  let canceledOrders = [];

  async function fetchOrders() {
    try {
      const response = await fetch('http://127.0.0.1:8000/orders/all/');
      const data = await response.json();
      activeOrders = data.active_orders;
      canceledOrders = data.canceled_orders;
      totalItems = activeOrders.reduce((sum, order) => sum + Object.values(order.order_items).reduce((a, b) => a + b, 0), 0);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  }

  async function placeOrder() {
    try {
      const response = await fetch('http://127.0.0.1:8000/orders/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_text: orderText })
      });
      if (response.ok) {
        orderText = '';
        fetchOrders();
      }
    } catch (error) {
      console.error('Error placing order:', error);
    }
  }

  onMount(fetchOrders);
</script>

<main>
  <h1>Drive-Through Orders</h1>
  <p><strong>Total Items Ordered:</strong> {totalItems}</p>
  
  <h2>Active Orders</h2>
  <ul>
    {#each activeOrders as order}
      <li>Order #{order.order_no}: {JSON.stringify(order.order_items)}</li>
    {/each}
  </ul>

  <h2>Canceled Orders</h2>
  <ul>
    {#each canceledOrders as order}
      <li>Order #{order.order_no}: {JSON.stringify(order.order_items)}</li>
    {/each}
  </ul>

  <h2>Place a New Order</h2>
  <input type="text" bind:value={orderText} placeholder="Enter order details..." />
  <button on:click={placeOrder}>Submit Order</button>
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
    display: block;
    width: 100%;
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
</style>
