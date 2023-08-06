import os

# from sqlalchemy.engine import Engine
#
# from youte.database import set_up_database
# from youte.cli import full_search
#
# API_KEY = os.environ["STAGING_API_KEY"]
#
#
# def test_create_tables(path="test.db"):
#     engine = set_up_database(path)
#     assert os.path.exists(path)
#     assert isinstance(engine, Engine)
#     os.remove(path)
#
#
# def test_full_search(path="test.db"):
#     full_search(
#         query="harry potter",
#         key=API_KEY,
#         max_pages=2,
#         outdb=path
#     )
#     assert os.path.exists(path)