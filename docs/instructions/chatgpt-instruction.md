# Install the CCDI Federation AI Skill in ChatGPT

The **CCDI Federation AI Copilot Skill** allows ChatGPT to query the CCDI Data Federation API and help analyze federation data.

## Install the Skill

1. Go to the **CCDI Federation AI GitHub repository**.

2. Download:
   `ccdi-federation-ai-copilot.zip`

3. Open **ChatGPT** and go to **Plugins → Skills**.

4. Make sure the **Skill Creator** skill is available.

5. Start a new **Work** chat and select **Skill Creator**.

6. Attach `ccdi-federation-ai-copilot.zip` to the chat.

7. Enter:

   `Install this agent skill into the Codex skill directory.`

8. Wait for ChatGPT to confirm that the skill was installed.

9. Go back to **Plugins → Skills** and verify that **CCDI Federation AI Copilot Skill** appears in the installed skills list.

## Use the Skill

Start a new chat and select the **CCDI Federation AI Copilot Skill**.

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


<div style="padding:60.91% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1221827407?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="fedration-agent-skill-install"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>


## References

* [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
