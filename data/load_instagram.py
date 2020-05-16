import instaloader as instl

username = "marvel"

L = instl.Instaloader(download_geotags=False,
                      download_comments=False,
                      download_videos=False,
                      download_video_thumbnails=False,
                      save_metadata=False)

profiles = {L.check_profile_id(username)}
L.download_profiles(profiles, profile_pic=False, fast_update=False, raise_errors=True, stories=False)