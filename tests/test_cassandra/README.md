Test Cassandra cluster database with 2 nodes.

```sh
# Create folders to mount Cassandra nodes on
mkdir node{1,2}
docker-compose up -d
```

Useful [recoure on Cassandra tombstones](https://opencredo.com/blogs/cassandra-tombstones-common-issues/)