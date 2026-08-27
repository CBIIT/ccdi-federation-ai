# Install the CCDI Federation AI Skill in ChatGPT

The **CCDI Federation AI Copilot Skill** allows ChatGPT to query the CCDI Data Federation API and help analyze federation data.

## Install the Skill

1. Go to the <a href="https://github.com/CBIIT/ccdi-federation-ai" target="_blank"><strong>CCDI Federation AI GitHub repository</strong></a>.

2. Download: <a href="https://github.com/CBIIT/ccdi-federation-ai/blob/main/ccdi-federation-ai-copilot.zip" target="_blank"><code>ccdi-federation-ai-copilot.zip</code></a>

3. Open **ChatGPT** and go to **Plugins → Skills**.

4. Click the **Add** button in the top-right corner and choose Create skill. This will start a new chat with **Skill Creator** selected.

5. Attach `ccdi-federation-ai-copilot.zip` to the chat.

6. Enter:

   `Install this agent skill into the Codex skill directory.`

7. Wait for ChatGPT to confirm that the skill was installed.

8. Go back to **Plugins → Skills** and verify that **CCDI Federation AI Copilot Skill** appears in the installed skills list.

## Use the Skill

Start a new chat and use the forward slash (/) to select the **CCDI Federation AI Copilot Skill**.

You can then ask questions in natural language, for example:

- `How many participants are in the federation?`
- `How many samples does the federation have?`
- `Count samples by federation node.`
- `Give me a bar chart of the sample counts by node.`

The skill will determine the appropriate CCDI Federation API query, retrieve the data, and present the results in ChatGPT.

## Example

Ask:

`How many samples does the federation have?`

Then follow up with:

`Give me a bar chart of this data.`

ChatGPT can use the same federation results to generate the visualization.


## References

- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
