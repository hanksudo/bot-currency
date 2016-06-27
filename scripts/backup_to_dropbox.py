import sys
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


# (https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/)
TOKEN = ""
LOCAL_FOLDER = "."


def upload_file(filename):
    with open(filename, "r") as f:
        try:
            print "Uploading file: {}".format(filename)
            dbx.files_upload(f, "/{}".format(filename), mode=WriteMode("overwrite"))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


if __name__ == "__main__":
    dbx = dropbox.Dropbox(TOKEN)

    # check token
    try:
        dbx.users_get_current_account()
    except AuthError:
        sys.exit("Invalid access token")

    entries = dbx.files_list_folder("").entries

    for (dirpath, dirnames, filenames) in os.walk(LOCAL_FOLDER):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            # only upload file with CSV extension
            if ext == ".csv" and filename not in entries:
                upload_file(filename)
