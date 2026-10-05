import json
class CleanString:
    def __init__(self,llm_reponse)->None:
        self.llm_reponse = llm_reponse

    @property
    def get_clean_llm_response(self)-> list:
        clean_Response = self.llm_reponse.replace("```json","").replace("```","").strip()
        response= json.loads(clean_Response)
        if isinstance(response, list):
            return response
        raise ValueError("not a list")


if __name__ == "__main__":
    obj = CleanString("""```json[{"id": "REQ-1", "section": "1.1", "text": "Log access."}]```""")
    print(obj.get_clean_llm_response)