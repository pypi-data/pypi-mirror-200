import os
import instaloader
import time

class Tools:
    def __init__(self, username, targetUsername):
        self.username = username
        self.targetUsername = targetUsername
        self.cwd = os.getcwd()
        self.basename = "pypanelMedia/Instagram/Profiles/"

    def comparator2000(self) -> str:
        '''
        This function check if the ```targetUsername`` folder exists, if not, create one and enter.
        '''
        # Check if exists, if not, create.
        if not os.path.exists(self.basename + self.targetUsername):
            os.makedirs(self.basename + self.targetUsername)

        # Change directory to targetUsername
        os.chdir(self.basename + self.targetUsername)
        return str(f"Im here {os.getcwd()}, tick.")

    def writeUserMD(self):
        self.comparator2000()
        L = instaloader.Instaloader()
        L.load_session_from_file(self.username)
        profileData = instaloader.Profile.from_username(L.context, self.targetUsername)
        # This will download only the user profile to a pretty json file.
        instaloader.save_structure_to_file(profileData, f"{self.targetUsername}.json")
        def entities(Profile) -> str:
            if len(Profile._metadata('biography_with_entities')["entities"]) == 0:
                return "No sponsors list."
            else:
                # If so, create the list/single string and return it.
                sponsorsList = ""
                for item in Profile._metadata('biography_with_entities')["entities"]:
                    sponsorsList = sponsorsList + f'{item["user"]["username"]}\n'
                return sponsorsList
        # This will write the resume of the profile in a text file.
        with open(f"{self.targetUsername}_resume.txt", "w", encoding="utf-8") as f:
            f.writelines(f"{profileData.full_name}\nTotal posts: {profileData.mediacount}\nTotal Followers: {profileData.followers}\nFollowing: {profileData.followees}\n{profileData.biography}\n{profileData.external_url}\nSponsors:\n{entities(profileData)}")
            f.close()
        os.chdir(self.cwd)
        return 0

    def downloadPosts(self):
        L = instaloader.Instaloader()
        L.load_session_from_file(self.username)
        L.dirname_pattern = self.basename + '{profile}/Posts/'
        L.filename_pattern = '{date_utc:%Y}/{date_utc:%m}/{date_utc:%d}/{date_utc}'
        L.save_metadata = True

        L.download_profiles([instaloader.Profile.from_username(L.context, self.targetUsername)], profile_pic=False, posts=True)
        return 0

    def downloadStories(self):
        L = instaloader.Instaloader()
        L.load_session_from_file(self.username)
        L.dirname_pattern = self.basename + '{profile}/Stories/'
        L.filename_pattern = '{date_utc:%Y}/{date_utc:%m}/{date_utc:%d}/{date_utc}'
        L.save_metadata = True

        L.download_stories([instaloader.Profile.from_username(L.context, self.targetUsername)])
        return 0

    def downloadProfilepic(self):
        L = instaloader.Instaloader()
        L.load_session_from_file(self.username)
        L.dirname_pattern = self.basename + '{profile}/Profile Pictures/'

        L.download_profilepic(instaloader.Profile.from_username(L.context, self.targetUsername))
        return 0

    def downloadHighLights(self):
            L = instaloader.Instaloader()
            L.load_session_from_file(self.username)
            profile = instaloader.Profile.from_username(L.context, self.targetUsername)
            highlights = L.get_highlights(profile)

            for highlight in highlights:
                title = highlight.title.replace(".", "Point")
                for item in highlight.get_items():
                    L.dirname_pattern = self.basename + "{profile}/Hightlights/"
                    L.filename_pattern = f"{title}/" + "{date_utc}"
                    L.download_storyitem(item, None)
                    time.sleep(2)
            

def test():
    username = input("Username use to download: ")
    targetUsername = input("Target:")
    tools = Tools(username, targetUsername)
    tools.writeUserMD()

    
if __name__ == "__main__":
    test()