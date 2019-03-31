from pydriller import RepositoryMining
import json


class RepoStats:
    def __init__(self, *args, **kwargs):
        self.commits_with_tests = 0
        self.total_commits = 0
        self.total_lines_net = 0
        self.test_lines_net = 0
        self.test_lines_per_commit = []
        self.total_lines_per_commit = []
        self.test_files = {}
        self.total_files = 0
        self.commits = {}
        self.repo = None
        return super().__init__(*args, **kwargs)    
    def analyze(self, repo_path):
        self.repo = RepositoryMining(repo_path, only_in_branch='master', only_modifications_with_file_types=['.py', '.java'])
    
        for commit in self.repo.traverse_commits():
            self.analyze_commit(commit)         
            self.total_commits += 1
        file_out = {
            "commits_with_tests":self.commits_with_tests,
            "total_commits" : self.total_commits,
            "total_lines": self.total_lines_net,
            "test_lines": self.test_lines_net,
            "number_of_test_files": len(self.test_files.keys()),
            "number_of_total_files": len(self.total_files.keys()),
            'test_lines_per_commit': self.test_lines_per_commit,
            'total_lines_per_commit': self.total_lines_per_commit
        }
        file = open(extractRepoName(repo_path)+'.json', 'w')
        file.write(json.dumps(file_out, indent=1))
        file.close()

    def check_test_path(self, path: str):
        return 'test' in path

    def check_test_filename(self, file_name: str):
        return 'test_' in file_name

    def count_modification_stats(self,modification, commit):
        if self.commits.get(commit.hash) is None:
            self.commits[commit.hash] = True
            self.commits_with_tests += 1
        # get test lines
        self.test_lines_net += modification.added - modification.removed
        
    def analyze_commit(self, commit):
        test_lines_in_commit = 0
        total_lines_in_commit = 0
        for modification in commit.modifications:
            if modification.new_path is not None and (self.check_test_path(modification.new_path) and self.check_test_filename(modification.filename)):
                full_path = modification.new_path
                self.count_modification_stats(modification, commit)
                test_lines_in_commit += modification.added - modification.removed
                if self.test_files.get(full_path) is None:
                    self.test_files[full_path] = 1
                else:
                    self.test_files[full_path] += 1
        
            if modification.new_path is None and (self.check_test_path(modification.old_path) and self.check_test_filename(modification.filename)):
                    full_path = modification.old_path
                    self.count_modification_stats(modification, commit)
                    test_lines_in_commit += modification.added - modification.removed
                    if self.test_files.get(full_path) is None:
                        self.test_files[full_path] = 1
                    else:
                        self.test_files[full_path] += 1
            total_lines_in_commit += modification.added - modification.removed
            self.total_lines_net += modification.added - modification.removed

            if modification.ModificationType == 1:  # Added
                self.total_files += 1
            if modification.ModificationType == 4:  # Deleted
                self.total_files -= 1



        self.test_lines_per_commit.append(test_lines_in_commit)
        self.total_lines_per_commit.append(total_lines_in_commit)

        
        
def extractRepoName(url):
    url = url.split(".git")[0]
    url = url.split("/")[-1]
    return url


def main():
    repoURLs = [
        "https://github.com/pallets/flask.git",
        "https://github.com/nvbn/thefuck.git",
        "https://github.com/jakubroztocil/httpie.git",
    ]

    for repo in repoURLs:
        repo_stats = RepoStats()
        repo_stats.analyze(repo)
        print("Done {}".format(repo))

main()
