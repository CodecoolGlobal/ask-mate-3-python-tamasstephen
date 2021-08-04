
def sort_questions(questions, sort_key="submission_time_desc"):
    sort_by_key = {
            "submission_time": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=False),
            "submission_time_desc": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=True),
            "vote_number": sorted(questions, key=lambda x: int(x["vote_number"])),
            "vote_number_desc": sorted(questions, key=lambda x: int(x["vote_number"]), reverse=True),
            "view_number": sorted(questions, key=lambda x: int(x["view_number"])),
            "view_number_desc": sorted(questions, key=lambda x: int(x["view_number"]), reverse=True),
            "title": sorted(questions, key=lambda x: x["title"]),
            "title_desc": sorted(questions, key=lambda x: x["title"], reverse=True),
            "message": sorted(questions, key=lambda x: x["message"]),
            "message_desc": sorted(questions, key=lambda x: x["message"], reverse=True)
            }
    return sort_by_key[sort_key]
