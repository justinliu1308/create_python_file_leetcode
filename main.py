import requests
import os
import sys
import textwrap
from bs4 import BeautifulSoup

def main(link):
    def api_query(link):
        # Format problem name for query and obtain structured filename for local file creation

        # Extract problem name (ex: find-the-town-judge) from URL for query
        split_link = link.split('/')
        problem_name = split_link[4]

        # Query for leetcode.com/graphql
        query_question_data = (
            "query questionData($titleSlug: String!) {"
                "\n  question(titleSlug: $titleSlug) {"
                    "\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    "
                    "translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    "
                    "isLiked\n    similarQuestions\n    contributors {"
                        "\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    "
                    "}\n    "
                    "langToValidPlayground\n    topicTags {"
                        "\n      name\n      slug\n      translatedName\n      __typename\n    "
                    "}\n    "
                    "companyTagStats\n    codeSnippets {"
                        "\n      lang\n      langSlug\n      code\n      __typename\n    "
                    "}\n    "
                    "stats\n    hints\n    solution {"
                        "\n      id\n      canSeeDetail\n      __typename\n    "
                    "}\n    "
                    "status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    "
                    "enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  "
                "}\n"
            "}\n"    
        )
        data = {
            "operationName": "questionData",
            "variables": {
                "titleSlug": problem_name
            },
            "query": query_question_data
        }
        r = requests.post('https://leetcode.com/graphql', json = data).json()
        soup = BeautifulSoup(r['data']['question']['content'], 'lxml')

        # Extract problem title, level of difficulty, and question prompt from query
        number = r['data']['question']['questionFrontendId']
        title = r['data']['question']['title'] + '.py'
        filename = number + ' ' + title
        difficulty = r['data']['question']['difficulty']
        question =  soup.get_text().replace('\n',' ')
        question = question.split('Example')[0][:-1]        # splice to drop the unnecessary special character
        question_lines = textwrap.wrap(question, width = 135)
        return split_link, filename, difficulty, question_lines

    def check_file_exists(filename):
        # Check if filename already exists, and if yes, do nothing to prevent file overwrite and data loss
        if filename in os.listdir():
            return True
        else:
            return False

    def create_local_file(split_link, filename, difficulty, question_lines):
        # Create a LeetCode problem local Python file
        # if 'description' in link: link = link[:-12]     # https:// ...problem-name/description/ isn't necessary, just ..problem-name/ is sufficient
        # 9/24/23 update - need to handle other forms of links such as query links: https://...problem-name/?envType=daily-question
        link = split_link[0] + split_link[2] + split_link[3] + split_link[4]
        new_file = open(filename, 'w')
        new_file.write('# ' + link + '\n# ' + difficulty + '\n\n')
        for line in question_lines:
            new_file.write('# ' + line + '\n')
        new_file.write('\n# My code:\n\n')
        new_file.close()

    split_link, filename, difficulty, question_lines = api_query(link)
    exist = check_file_exists(filename)
    if exist == True:
        print(f"{filename} already exists. Nothing was done in order to prevent file overwrite.\nPulling existing file...")
    else:
        create_local_file(split_link, filename, difficulty, question_lines)
        print("New file created:", filename, "\nOpening new file...")

    # Open the file in new tab
    os.startfile(filename)

if __name__ == "__main__":
    # https://leetcode.com/problems/same-tree/
    if len(sys.argv) == 2:
        link = str(sys.argv[1])
        try:
            main(link)
        except:
            print("Fatal error creating LeetCode file")
    else:
        print("Please provide a valid website URL as an argument to run the program.\n")

    # Testing - will generate 10 different files. Need to visually verify.

    # main('https://leetcode.com/problems/same-tree/')
    # main('https://leetcode.com/problems/minimum-falling-path-sum/')
    # main('https://leetcode.com/problems/minimum-path-sum/')
    # main('https://leetcode.com/problems/product-of-the-last-k-numbers/description/')
    # main('https://leetcode.com/problems/number-of-arithmetic-triplets/')
    # main('https://leetcode.com/problems/stone-game-ii/')
    # main('https://leetcode.com/problems/stone-game-ix/')
    # main('https://leetcode.com/problems/can-i-win/')
    # main('https://leetcode.com/problems/satisfiability-of-equality-equations/')
    # main('https://leetcode.com/problems/word-search/')
    # main('https://leetcode.com/problems/find-the-difference/?envType=daily-question')
    