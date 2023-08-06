QUERY = """
    query questionEditorData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        codeSnippets {
            lang
            langSlug
            code
        }
        envInfo
        enableRunCode
    }
}
"""


def get_question_editor_data_query(problem_slug: str) -> dict[str, str]:
    return {"query": QUERY, "variables": {"titleSlug": problem_slug}}
