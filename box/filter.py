from datetime import datetime


class Filter:
    def _filter_by_author(self, commits: dict, author: str):
        filter_by_author = lambda cid: commits[cid]['author'] == author
        filtered_cid = filter(filter_by_author, commits)

        return {cid: commits[cid] for cid in filtered_cid}
    
    def _filter_by_email(self, commits: dict, email: str):
        filter_by_author = lambda cid: commits[cid]['author_email'] == email
        filtered_cid = filter(filter_by_author, commits)

        return {cid: commits[cid] for cid in filtered_cid}
