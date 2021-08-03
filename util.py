
def sort_questions(questions, sort_key="submission_time_desc"):
    sort_by_key = {
            "submission_time": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=False),
            "submission_time_desc": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True),
            "vote_number": sorted(questions, key=lambda x: int(x["vote_number"])),
            "vote_number_desc": sorted(questions, key=lambda x: int(x["vote_number"])),
            "view_number": sorted(questions, key=lambda x: int(x["vote_number"])),
            "title": sorted(questions, key=lambda x: x["title"]),
            "message": sorted(questions, key=lambda x: x["message"])
            }
    return sort_by_key[sort_key]
