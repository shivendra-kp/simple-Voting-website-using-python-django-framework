
from elections.models import BB
from backend.utils.crypto_hash import crypto_hash


def mine_block(last_block,election,candidate):
    hash = crypto_hash(last_block.h,election.name,candidate.name)
    block = BB(election=election,candidate=candidate,h=hash,lh=last_block.h)
    block.save()
    print("Successfully mined block")


def get_blockchain(election):
    chain = BB.objects.filter(election= election).order_by('id')
    return chain

def add_genesis(election):
    hash = crypto_hash(election.name)
    block = BB(election=election,candidate=None,lh="GENESIS",h="GENESIS")
    block.save()