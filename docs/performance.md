# Performance Evaluation and Measurements

## Objective

The goal of this section is to evaluate the impact of caching and replication on the performance of Bazar.com. This includes measuring average response times and the cost of maintaining cache consistency.

---

## Experiment 1: Response Time With vs Without Caching

### Method:

* We used Postman to send repeated GET requests to:

  * `/info/1`
  * `/search/<topic>`
* Measured response times over 10 iterations for each scenario.

### Results:

| Scenario        | Avg. Response Time (ms) |
| --------------- | ----------------------- |
| Without Caching | 190                     |
| With Caching    | 42                      |

### Conclusion:

Caching significantly reduces latency for read operations. In our test case, response time improved by over **75%**.

---

## Experiment 2: Cache Invalidation Overhead

### Method:

* We executed a PATCH request `/update` or a POST `/purchase/1` to trigger cache invalidation.
* Measured time to process the invalidation and subsequent read request.

### Results:

| Operation         | Invalidation Overhead (ms) | Post-invalidation Read Latency (ms) |
| ----------------- | -------------------------- | ----------------------------------- |
| Update via PATCH  | 38                         | 195                                 |
| Purchase via POST | 42                         | 192                                 |

### Conclusion:

Cache invalidation introduces a small overhead (\~40ms), but ensures strong consistency. The first read after invalidation experiences higher latency (similar to no-cache scenario).

---

## Summary Table

| Metric                      | Without Caching | With Caching | After Invalidation |
| --------------------------- | --------------- | ------------ | ------------------ |
| Avg. Read Latency           | 190 ms          | 42 ms        | 195 ms             |
| Cache Invalidation Overhead | N/A             | N/A          | \~40 ms            |

---

## Final Notes

* Our caching is time-based (TTL = 60s).
* Writes (purchase/update) always bypass the cache.
* Replication with fallback mechanism ensures availability.



