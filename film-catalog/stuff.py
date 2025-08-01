from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main() -> None:
    # some comment
    print(redis.ping())
    redis.set("name", "yaros")
    redis.set("temp", "qwerty")
    redis.set("abb", "aaa")
    redis.set("num", "40")

    print("name:", redis.get("name"))

    print(redis.getdel("name"))
    print(
        [
            redis.get("name"),
            redis.get("temp"),
            redis.get("abb"),
            redis.get("aaa"),
        ],
    )
    redis.delete("temp")
    print(redis.keys("*"))


if __name__ == "__main__":
    main()
