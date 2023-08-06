import json

import requests

from .queries.question_editor_data import get_question_editor_data_query


LEETCODE_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com/problems",
}


class TemplateService:
    def _get_template_code(self, problem_slug: str, lang: str):
        query = get_question_editor_data_query(problem_slug)

        response = requests.post(
            LEETCODE_URL,
            json=query,
            headers=HEADERS,
        )
        json_response = json.loads(response.text)

        code_snippets = json_response["data"]["question"]["codeSnippets"]

        template = next(
            (
                code_snippet["code"]
                for code_snippet in code_snippets
                if code_snippet["lang"] == lang
            ),
            None,
        )

        return template

    def _get_lang_layout(self, lang: str):
        return {
            "C++": "cpp",
            "Java": "java",
            "Python": "python",
            "Kotlin": "kotlin",
            "Rust": "rust",
        }[lang] + ".layout"

    def get_template(self, problem_slug: str, lang: str):
        code = self._get_template_code(problem_slug, lang)

        layout_name = self._get_lang_layout(lang)

        with open(f"./services/template_service/layouts/{layout_name}", "r") as fd:
            layout_code = fd.read()
            layout_code = layout_code.replace("{{code}}", code)

        return layout_code
