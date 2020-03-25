import json
import pathlib

class Groups:
    groups_listing_file = f'{pathlib.Path(__file__).parent.absolute()}/eclipse_groups_listing.json'
    def __init__(self):
        with open(self.groups_listing_file, 'r') as f:
            self.groups = json.load(f)

    def get_categories(self):
        categories = []
        for group in self.groups["groups_information"]:
            for folder in group["folders"]:
                if len(folder["category"]) > 0:
                    categoryStr = folder["category"].replace("(","").replace(")","")
                    categoryList = categoryStr.split(" ")
                    for cat in categoryList:
                        if cat not in categories and cat not in ["and", "or"]:
                            categories.append(cat)
        categories.sort()
        return categories

    def add_group(self, group_info):
        self.groups["groups_information"].append(group_info)
        self.save_json()

    def save_json(self):
        json_file = open(self.groups_listing_file, 'w')
        json_file.write(json.dumps(self.groups, indent=2))
        json_file.close()

    def delete_folders_by_filter(self, filter_str):
        print("Enter is interpretted the same way as no.")
        for group in self.groups["groups_information"]:
            newFolders = []
            for folder in group["folders"]:
                if addFolderCheck(folder["folder_name"], group["group_name"], filter_str):
                    newFolders.append(folder)
            group["folders"] = newFolders
        self.save_json()

    def go_through_empty_categories(self):
        print("Leave blank to delete folder")
        for group in self.groups["groups_information"]:
            newFolders = []
            promptContinue = False
            alreadyPrinted = False
            print(f"\n⭐{group['group_name']}")
            for folder in group["folders"]:
                if folder["category"] != "UNSELECTED":
                    newFolders.append(folder)
                else:
                    if not alreadyPrinted:
                        for folderListing in group["folders"]:
                            print(f"-- {folderListing['folder_name']}")
                        print("-------------------")
                        alreadyPrinted = True
                    promptContinue = True
                    result = input(f"'{folder['folder_name']}'. Category? : ")
                    if result != "":
                        folder["category"] = result
                        newFolders.append(folder)
            group["folders"] = newFolders
            if promptContinue:
                cont = input("Continue? 'EXIT to leave: ")
                if cont == "EXIT":
                    break
        self.save_json()

def addFolderCheck(folderName, groupName, filterStr):
    lowerFolderName = folderName.lower()
    lowerFilter = filterStr.lower()
    if lowerFolderName == lowerFilter:
        return False
    if lowerFilter in lowerFolderName:
        result = input(f"{groupName} ::: '{folderName}'. Add? (Yes/No): ")
        if result == "Yes":
            return True
        elif result == "No":
            return False
    return True
