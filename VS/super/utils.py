from .models import VoterIdCount

def generatevid(region):
    t1 = region.name[:2].upper()
    t2= region.state[:2].upper()

    vc=VoterIdCount.objects.filter(region=region).first()
    if vc == None:
        vc = VoterIdCount(region=region)

    t3=str(vc.count)
    vid =t1+t2+t3

    vc.count+=1
    vc.save()
    return vid