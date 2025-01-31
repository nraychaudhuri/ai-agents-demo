from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

serp_api_key = "<your api key>"

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="the search query")

class MyCustomTool(BaseTool):
    name: str = "SerpAPITool"
    description: str = (
        "A tool that can be used to search the internet with a query."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def googleSearch(self, query, timeFrame, count, qdrType="m", location=""):
        print(">>>>>> google search query ")
        print(query)
        print(">>>>>> ")
        params = {
            "api_key": serp_api_key,
            "engine": "google",
            "google_domain": "google.com",
            "q": query,
            "location": location,
            "tbs": f"qdr:{qdrType}{timeFrame}",
            "gl": "us",
            "hl": "en",
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        print(organic_results)
        # string = []
        # for result in results:
        #     try:
        #         string.append(
        #             "\n".join(
        #                 [
        #                     f"Title: {result['title']}",
        #                     f"Link: {result['link']}",
        #                     f"Snippet: {result['snippet']}",
        #                     "---",
        #                 ]
        #             )
        #         )
        #     except KeyError:
        #         continue

        transformed_list = [
            "\n".join([f"title: {website['title']}", f"link: {website['link']}", f"snippet: {website['snippet']}"])
            for website in organic_results
        ]
        content = "\n".join(transformed_list[:count])
        return f"\nSearch results: {content}\n"
    def _run(self, argument: str) -> str:
        # Implementation goes here
        return self.googleSearch(argument, 6, 5)
        # return "this is an example of a tool output, ignore it and move along."
