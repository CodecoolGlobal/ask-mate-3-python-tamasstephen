
def sort_questions(questions, sort_key, descending=True):
    sort_by_key = {
            "submission_time": sorted(questions, key=lambda x: int(x["submission_time"]), reverse=descending),
            "vote_number": sorted(questions, key=lambda x: int(x["vote_number"]), reverse=descending),
            "view_number": sorted(questions, key=lambda x: int(x["vote_number"]), reverse=descending),
            "title": sorted(questions, key=lambda x: x["title"], reverse=descending),
            "message": sorted(questions, key=lambda x: x["message"], reverse=descending)
            }
    return sort_by_key[sort_key]
