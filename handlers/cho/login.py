from quart import Blueprint, request
from objects import glob
import os
from handlers.response import Failed, Success
from argon2 import PasswordHasher
import time
import utils

ph = PasswordHasher()
bp = Blueprint("login", __name__)

php_file = True


@bp.route("/", methods=["POST"])
async def login():
    params = await request.form

    if "username" not in params or len(params["username"]) == 0:
        return Failed("Invalid username.")

    p = glob.players.get(name=params["username"])

    if not p:
        return Failed("User not found.")
    if params["version"] != "3":
        return Failed("This client is outdated")

    res = await glob.db.fetch(
        "SELECT password_hash, status FROM users WHERE id = $1", [p.id]
    )
    status = res["status"]
    pswd_hash = res["password_hash"]
    hashes = glob.cache["hashes"]

    if pswd_hash in hashes:
        if params["password"] != hashes[pswd_hash]:
            return Failed("Wrong password.")
    else:
        try:
            ph.verify(pswd_hash, params["password"])
        except:
            return Failed("Wrong password.")

        hashes[pswd_hash] = params["password"]

    if status != 0:
        return Failed("Banned.")

    # update last ping
    p.last_online = time.time()

    # make uuid if havent
    if not p.uuid:
        p.uuid = utils.make_uuid(p.name)

    if os.path.isfile(f"data/avatar/{p.id}.png"):
        p.avatar = f"{glob.config.host}/user/avatar/{p.id}.png"
    else:
        p.avatar = f"https://s.gravatar.com/avatar/{p.email_hash}"
    # returns long string of shit
    return Success(
        "{id} {uuid} {rank} {rank_by} {acc} {name} {avatar}".format(
            id=p.id,
            uuid=p.uuid,
            rank=p.stats.rank,
            rank_by=int(p.stats.rank_by),
            acc=p.stats.droid_acc,
            name=p.name,
            avatar=p.avatar,
        )
    )
