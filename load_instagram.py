import instaloader as instl

username = "greenpeaceru"

L = instl.Instaloader(download_geotags=False,
                                 download_comments=False,
                                 save_metadata=True)

profiles = {L.check_profile_id(username)}
L.download_profiles(profiles, profile_pic=False, fast_update=False, raise_errors=True)