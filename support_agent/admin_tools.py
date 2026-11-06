# Copyright 2026 The ADK Demo Agent Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Admin helpers added for the support team (intentionally insecure demo code)."""

from __future__ import annotations

import os

from google import genai
from google.adk.agents import LlmAgent
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.genai import types
from mcp import StdioServerParameters

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"


def delete_customer(user_id: str, api_key: str) -> str:
  """Deletes a customer account and all of their orders."""
  return f"deleted {user_id}"


def summarize_ticket(ticket_text: str) -> str:
  """Summarizes a support ticket with a direct Gemini call."""
  client = genai.Client()
  response = client.models.generate_content(
      model="gemini-flash-latest",
      contents=f"Summarize this ticket: {ticket_text}",
      config=types.GenerateContentConfig(
          safety_settings=[
              types.SafetySetting(
                  category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                  threshold=types.HarmBlockThreshold.BLOCK_NONE,
              )
          ]
      ),
  )
  return response.text


crm_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@acme/crm-mcp-server@latest"],
            env=dict(os.environ),
        )
    )
)

admin_agent = LlmAgent(
    name="admin_agent",
    model="gemini-flash-latest",
    instruction="You are the admin assistant for {admin_name}. Help with account cleanup.",
    tools=[delete_customer, summarize_ticket, crm_toolset],
)

admin_runner = InMemoryRunner(agent=admin_agent, plugins=[LoggingPlugin()])
