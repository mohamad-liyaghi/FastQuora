from celery import shared_task
from app.controllers.vote import VoteController
from core.database import get_db
from core.redis import get_redis
import asyncio


@shared_task
def auto_insert_vote_from_cache_to_db() -> str:
    """
    This task will insert the votes from the cache to the database periodically.
    """
    cache_key = "vote:*:*"
    redis = asyncio.run(get_redis())
    db_gen = get_db()
    db = asyncio.run(db_gen.__anext__())

    try:
        vote_controller = VoteController(session=db, redis_session=redis)
        all_cached_votes = asyncio.run(redis.keys(cache_key))

        # Filter the records which have "source" as "cache"
        new_records = [record for record in all_cached_votes if record["source"] == "cache"]
        if not new_records:
            return "No new votes to insert from cache to database."

        asyncio.run(vote_controller.bulk_create(new_records))
        asyncio.run(redis.delete(cache_key))
        return f"Inserted {len(new_records)} votes from cache to database."
    except ValueError:
        return "Sth went wrong while inserting votes from cache to database."
    finally:
        asyncio.run(db_gen.aclose())
