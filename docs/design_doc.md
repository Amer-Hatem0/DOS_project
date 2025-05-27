**Design Document - Lab 2: Bazar.com Replication, Caching, and Consistency**

---

**1. Overview of the Program Design**

This project re-architects the original Bazar.com online bookstore to improve scalability and response time under higher workloads. The system was decomposed into multiple microservices, and replication, caching, and containerization using Docker were implemented.

**System Components:**

* **CatalogService (2 replicas)**: Handles book information queries and updates.
* **PurchaseService (2 replicas)**: Handles item purchases and updates the catalog.
* **FrontEnd (1 instance)**: Acts as the entry point for users. Implements in-memory caching and request forwarding using basic load balancing.

All services communicate using RESTful APIs.

---

**2. How It Works**

* **FrontEnd Service** receives user requests for:

  * Searching books by topic.
  * Getting info about a specific item.
  * Purchasing an item.

* **Caching**:

  * Implemented inside the FrontEnd.
  * Caches `/search/<topic>` and `/info/<item_id>` requests for 60 seconds.
  * Automatically invalidated when an item is updated or purchased (via explicit `/invalidate/<item_id>` POST calls).

* **Load Balancing**:

  * FrontEnd selects one of the two catalog or purchase services using a fallback strategy (try first, fallback to second if fails).
  * Requests are retried in case of backend unavailability.

* **Database Synchronization**:

  * Both replicas of each service access the same mounted SQLite file (using Docker volume `/data`) to simulate a synchronized replicated database.

* **Cache Consistency**:

  * On every purchase or catalog update, the backend sends a POST request to `/invalidate/<item_id>` on the FrontEnd.
  * This removes the relevant item/topic from cache.

* **Dockerization**:

  * Each component is containerized using a custom Dockerfile.
  * `docker-compose.yml` defines the multi-container deployment.
  * Volumes are mounted for shared database access across replicas.

---

**3. Tradeoffs Considered**

| Feature            | Choice Made               | Tradeoff Explanation                                              |
| ------------------ | ------------------------- | ----------------------------------------------------------------- |
| Caching strategy   | In-memory (TTL 60s)       | Simple and fast, but loses cache after restart                    |
| Replication        | Two replicas per service  | Simulates real-world redundancy, but not truly distributed        |
| Cache invalidation | Manual push from backends | Ensures strong consistency, but relies on success of notify calls |
| Database           | Shared volume (SQLite)    | Easy to simulate sync, not realistic for true distributed systems |
| Load balancing     | Try-first fallback        | Simple to implement, may overuse the first replica                |

---

**4. Possible Improvements**

1. **Advanced Load Balancing**:

   * Round-robin or least-loaded strategies for fairer distribution.
   * Maintain request counters or implement a lightweight balancer.

2. **Persistent Caching**:

   * Use Redis or file-based cache to persist across container restarts.

3. **Database Replication**:

   * Replace shared SQLite volume with real replication (e.g., PostgreSQL master-slave).

4. **Service Discovery**:

   * Use DNS-based discovery or service mesh (e.g., Consul, Istio).

5. **Testing and Monitoring**:

   * Add logging middleware, rate limits, and Prometheus/Grafana for monitoring.

---

**5. How to Run the Program**

**Requirements:**

* Docker
* Docker Compose

**Steps:**

1. Clone the repository:

```bash
git clone <your_repo_url>
cd project_folder
```

2. Start the system:

```bash
docker-compose up --build
```

3. Access the gateway:

```
http://localhost:8080
```

4. Use Postman or CURL to test endpoints:

* `GET /search/<topic>`
* `GET /info/<item_id>`
* `POST /purchase/<item_id>`

5. To stop:

```bash
docker-compose down
```

---

**6. Directory Structure**

```
.
├── catalogservice/
├── catalogservice2/
├── purchase/
├── purchase2/
├── front/
├── data/               # Shared SQLite files
├── docker-compose.yml
├── docs/
│   ├── design_doc.md   # This file
│   ├── output.txt      # Screenshots or logs
│   └── performance.md  # Performance comparison
```

---

**End of Design Document**


