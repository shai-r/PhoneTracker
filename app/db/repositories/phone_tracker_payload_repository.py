
from app.db.models import PhoneTrackerPayload
from app.db.repositories.neo4j_repository import insert_to_neo4j
from app.db.services.json_to_model_service import query_for_create_devices_and_connection, \
    convert_phone_tracker_payload_to_params


def insert_phone_tracker_payload(phone_tracker_payload: PhoneTrackerPayload):
    if phone_tracker_payload.from_device.id == phone_tracker_payload.to_device.id:
        return None
    return insert_to_neo4j(
        query=query_for_create_devices_and_connection,
        params=convert_phone_tracker_payload_to_params(phone_tracker_payload)
    ).map(lambda res: [
        dict(res["d1"]),
        dict(res["r"]),
        dict(res["d2"])
    ]).value_or(None)


#
# def get_all_cinemas():
#     with driver.session() as session:
#         query = "MATCH (all:Cinema) RETURN all"
#         res = session.run(query).data()
#         return t.pipe(
#             res,
#             t.partial(t.pluck, "all"),
#             list
#         )
#
#
# def find_cinema_by_uid(cinema_uid: str):
#     with driver.session() as session:
#         query = """
#             MATCH (c:Cinema{uid: $cinema_uid})
#             RETURN c
#         """
#         params = {"cinema_uid": cinema_uid}
#         res = session.run(query, params).single()
#         return (Maybe.from_optional(res)
#                 .map(itemgetter("c"))
#                 .map(lambda c: dict(c))
#                 .value_or({}))
#
# def update_cinema_by_uid(cinema_uid: str, cinema: Cinema):
#     with driver.session() as session:
#         query = """
#             MERGE (c:Cinema {uid: $cinema_uid})
#             SET c.name = $name, c.location = $location, c.capacity = $capacity
#             RETURN c
#         """
#         params = {
#             "cinema_uid": cinema_uid,
#             "name": cinema.name,
#             "location": cinema.location,
#             "capacity": cinema.capacity
#         }
#         res = session.run(query, params).single()
#         return (Maybe.from_optional(res)
#                 .map(itemgetter("c"))
#                 .map(lambda c: dict(c))
#                 .value_or({}))
#
#
# def delete_cinema_by_uid(cinema_uid: str):
#     with driver.session() as session:
#         query = """
#             MATCH (c:Cinema {uid: cinema_uid})
#             DETACH DELETE c
#             RETURN c
#         """
#         params = {
#             "cinema_uid": cinema_uid
#         }
#         res = session.run(query, params).single()
#         return True if res else False
#
#
# def delete_all_cinemas():
#     with driver.session() as session:
#         query = """
#             MATCH (c:Cinema)
#             DETACH DELETE c
#             RETURN c
#         """
#         res = session.run(query).data()
#         print(res)
#         return True if res else False