import sys
import pprint
from . import project_functions
from . import config as cfg


def event_val(event, field, obs_type: str = cfg.MEDIA):
    try:
        return event[cfg.PJ_OBS_FIELDS[obs_type][field]]
    except:
        return None


_, _, pj, _ = project_functions.open_project_json(sys.argv[1])

pprint.pprint(list(pj[cfg.OBSERVATIONS].keys()))

print()

obs_id = "images NO TIME"

pprint.pprint(pj[cfg.OBSERVATIONS][obs_id])

print(cfg.PJ_OBS_FIELDS[cfg.IMAGES][cfg.COMMENT])

print()

print(f"{pj[cfg.OBSERVATIONS][obs_id][cfg.EVENTS][0][cfg.PJ_OBS_FIELDS[cfg.IMAGES][cfg.BEHAVIOR_CODE]]=}")

print()


print(f"{event_val(pj[cfg.OBSERVATIONS][obs_id][cfg.EVENTS][0], cfg.BEHAVIOR_CODE, 18)=}")
