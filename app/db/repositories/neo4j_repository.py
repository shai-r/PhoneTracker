from returns.maybe import Maybe

from app.db.database import driver


def insert_to_neo4j(query: str, params: dict):
    with driver.session() as session:
        return (Maybe.from_optional(session.run(query, params).single())
                .map(lambda record: dict(record)
                     )
                )
