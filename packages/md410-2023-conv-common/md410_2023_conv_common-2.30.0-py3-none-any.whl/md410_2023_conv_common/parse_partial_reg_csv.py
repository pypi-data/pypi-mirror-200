import csv
from datetime import datetime

import models

from rich import print

with open("230402_2009_partial_registrations.csv", "r") as fh:
    c = csv.DictReader(fh)
    for r in c:
        d = {}
        for a in (
            "first_names",
            "last_name",
            "name_badge",
            "cell",
            "email",
            "dietary",
            "disability",
            "club",
        ):
            d[a] = r[f"main_{a}"]
        for a in ("mjf_lunch", "pdg_dinner", "beach_cleanup", "lpe_breakfast"):
            d[a] = bool(r[f"main_{a}"])
        d["lion"] = r["membership"] == "lion"
        pm = models.PartialAttendeeModel(**d)

        for k, v in (
            ("welcome", "welcome"),
            ("dist_conv", "dist_convention"),
            ("md_conv", "md_convention"),
            ("theme", "theme"),
            ("pins", "pins"),
        ):
            d[k] = int(r[v])
        pi = models.PartialRegistrationItems(**d)
        m = models.PartialRegistration(
            attendee=pm, items=pi, timestamp=datetime.fromisoformat(r["created_at"].rsplit(".")[0])
        )
        print(m)
