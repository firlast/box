from datetime import datetime


class Filter:
    def _filter_by_author(self, commits: dict, author: str) -> dict:
        filter_by_author = lambda cid: commits[cid]['author'] == author
        filtered_cid = filter(filter_by_author, commits)

        return {cid: commits[cid] for cid in filtered_cid}
    
    def _filter_by_email(self, commits: dict, email: str) -> dict:
        filter_by_author = lambda cid: commits[cid]['author_email'] == email
        filtered_cid = filter(filter_by_author, commits)

        return {cid: commits[cid] for cid in filtered_cid}

    def _filter_by_date(self, commits: dict, date: str) -> dict:
        def fbd(cid):
            commit_date = datetime.strptime(commits[cid]['date'], '%Y-%m-%d %H:%M:%S')
            return date == commit_date.strftime('%Y-%m-%d')

        filtered_commits = {cid: commits[cid] for cid in filter(fbd, commits)}
        return filtered_commits

    def filter(self, commits: dict, by_name: str = None,
               by_email: str = None, by_date: str = None) -> dict:
        filtered_commits = commits
        
        if by_name:
            filtered_commits = self._filter_by_author(filtered_commits, by_name)
        
        if by_email:
            filtered_commits = self._filter_by_email(filtered_commits, by_email)

        if by_date:
            filtered_commits = self._filter_by_date(filtered_commits, by_date)

        return filtered_commits
