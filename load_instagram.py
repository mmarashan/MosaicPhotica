import instaloader as instl

username = ""

L = instl.Instaloader(download_geotags=False,
                                 download_comments=False,
                                 save_metadata=True)

# login = ""
# password = ""
# try:
#     loader.login(login, password)
# except TwoFactorAuthRequiredException as e:
#     code = input("Input your digit code without space:")
#     loader.two_factor_login(code)

profiles = {L.check_profile_id(username)}
L.download_profiles(profiles, profile_pic=False, fast_update=False, raise_errors=True)
