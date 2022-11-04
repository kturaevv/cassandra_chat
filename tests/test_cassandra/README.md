Test Cassandra cluster database with 2 nodes.

```sh
# Create folders to mount Cassandra nodes on
mkdir node{1,2}
docker-compose up -d
```

### General rules to follow for good DB modelling:
* Balance partitions
* Minimize # of partitions read
* Model around QUERIES, not objects or relations
* N queries N tables

Useful [recoure on Cassandra tombstones](https://opencredo.com/blogs/cassandra-tombstones-common-issues/)