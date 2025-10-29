# OrderFlow – Real-Time Distributed Inventory System

**OrderFlow** is a real-time inventory management system built with **FastAPI**, **Redis Pub/Sub**, and **Supabase**. It demonstrates how multiple distributed services (store servers) can synchronize stock data in real time using an event-driven architecture. This project is ideal for understanding distributed systems, microservices, and real-time data updates.

---

## **Features**

* **Real-Time Stock Synchronization**
  Stock changes in one instance are instantly propagated to all other instances via Redis Pub/Sub.

* **Event-Driven Architecture**
  Uses Redis Pub/Sub to handle updates asynchronously, keeping multiple nodes in sync.

* **Microservice-Ready Design**
  Separates concerns using FastAPI routers, Redis messaging, and Supabase as the database.

* **RESTful API Endpoints**

  * Add a product
  * Update stock
  * View all products

* **Distributed System Simulation**
  Can run multiple FastAPI instances on different ports to simulate multiple stores sharing inventory data.

---

## **Tech Stack**

* **Python 3.11+**
* **FastAPI** – API framework
* **Redis** – Pub/Sub for event-driven communication
* **Supabase** – PostgreSQL database backend
* **Docker** *(optional)* – To simulate containerized deployments

---

## **Project Structure**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI entrypoint
│   ├── redis_pubsub.py    # Redis Pub/Sub utilities
│   └── routers/
│       ├── __init__.py
│       └── inventory.py   # Inventory API routes
├── database.py            # Supabase database functions
├── .env                   # Environment variables
└── ...
```

---

## **Setup Instructions**

### **1. Clone the repository**

```bash
git clone <your-repo-url>
cd orderflow/backend
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure environment**

Create a `.env` file with your Supabase credentials:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
REDIS_URL=redis://localhost:6379/0
```

### **4. Start Redis**

Run Redis server:

```bash
redis-server
```

### **5. Run FastAPI**

Single instance:

```bash
uvicorn app.main:app --reload --port 8000
```

Multiple instances (simulate distributed nodes):

```bash
uvicorn app.main:app --reload --port 8001
uvicorn app.main:app --reload --port 8002
```

### **6. Test API**

* Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Add a product, update stock, and check synchronization across instances.

---

## **How It Works**

1. **Adding/Updating Products**

   * FastAPI endpoints update Supabase.
   * The `publish_update()` function sends a message to Redis.

2. **Redis Pub/Sub**

   * All FastAPI instances subscribe to the `inventory_updates` channel.
   * When a message is published, all nodes update their local state immediately.

3. **Distributed Simulation**

   * Running multiple FastAPI instances simulates multiple stores connected to the same Redis and database.
   * Demonstrates event-driven architecture, real-time sync, and distributed system principles.

---

## **Future Improvements**

* Add **in-memory caching** for faster reads per node.
* Implement **Docker Compose** to containerize nodes and Redis.
* Add **monitoring** with Prometheus and Grafana.
* Support **order processing and customer checkout** in real time.

---

## **License**

MIT License – free to use and modify.

