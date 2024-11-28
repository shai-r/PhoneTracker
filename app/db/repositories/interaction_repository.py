from datetime import datetime


from app.db.database import driver


def is_concurrent_call(id1: str, id2: str, timestamp: datetime) -> bool:
    with driver.session() as session:
        query = """
            OPTIONAL MATCH (d1:Device {id: $id1}) 
                -[r1:CONNECTED {timestamp: $timestamp}]-> 
                (:Device) 
            OPTIONAL MATCH (:Device) 
                -[r2:CONNECTED {timestamp: $timestamp}]-> 
                (d1:Device {id: $id1})
            OPTIONAL MATCH (d2:Device {id: $id2}) 
                -[r3:CONNECTED {timestamp: $timestamp}]-> 
                (:Device)
            OPTIONAL MATCH (:Device) 
                -[r4:CONNECTED {timestamp: $timestamp}]-> 
                (d2:Device {id: $id2})
            RETURN 
                COUNT(r1) > 0 AS id1_connected,
                COUNT(r2) > 0 AS id1_incoming,
                COUNT(r3) > 0 AS id2_connected,
                COUNT(r4) > 0 AS id2_incoming
        """
        params = {
            "id1": id1,
            "id2": id2,
            "timestamp": timestamp
        }
        result = session.run(query, params).single()

        return any([
            result["id1_connected"],
            result["id1_incoming"],
            result["id2_connected"],
            result["id2_incoming"]
        ])
