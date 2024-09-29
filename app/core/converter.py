from app.models import Crew, CrewGlobal, SearchCrewsAllResponse

# TODO: 등록된 크루가 굉장히 많아지면 async
def crew_to_crewGlobal(source: list[Crew]) -> list[CrewGlobal]:
    result = []
    for s in source:
        s = s[0]
        result.append(CrewGlobal(crew_id=s.crew_id,
        name=s.name,
        contents=s.contents,
        sns=s.sns,
        region=s.region,
        image=s.image))
    return result

def crewGlobal_to_searchCrewsAllResponse(source: list[CrewGlobal]) -> list[SearchCrewsAllResponse]:
    result = []
    for s in source:
        result.append(SearchCrewsAllResponse(crew_id=s.crew_id,
        name=s.name,
        contents=s.contents,
        sns=s.sns,
        region=s.region,
        image_uri=s.image.file_uri if s.image else None))
    return result