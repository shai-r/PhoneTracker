from returns.maybe import Maybe

from app.db.database import driver


def connect_to_neo4j_return_single(query: str, params: dict):
    with driver.session() as session:
        return (Maybe.from_optional(session.run(query, params).single())
                .map(lambda record: dict(record)
                     )
                )

def connect_to_neo4j_return_data(query: str, params: dict = None):
    with driver.session() as session:
        if params:
            return session.run(query, params).data()
        return session.run(query).data()
